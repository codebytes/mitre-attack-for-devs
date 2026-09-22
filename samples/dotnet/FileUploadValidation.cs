using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Defense against T1505.003 (Web Shell).
///
/// The goal is NOT to recognise malicious content. Scanning an upload for strings
/// like "eval(" or "&lt;?php" fails in both directions: it flags legitimate PDFs and
/// office documents that happen to contain those bytes, and it misses anything
/// encoded, compressed, or simply spelled differently.
///
/// The durable control is structural. A web shell is only dangerous if the server
/// will execute it. Store uploads where nothing can execute them and the class of
/// attack goes away regardless of file content.
///
/// Reference: https://attack.mitre.org/techniques/T1505/003/
/// </summary>
public class UploadValidator
{
    private readonly UploadOptions _options;
    private readonly ILogger<UploadValidator> _logger;

    public UploadValidator(ILogger<UploadValidator> logger, UploadOptions? options = null)
    {
        _logger = logger;
        _options = options ?? new UploadOptions();
    }

    // Magic bytes for the formats we actually accept. This confirms the bytes match
    // the declared type; it is not a malware check and does not pretend to be one.
    private static readonly Dictionary<string, byte[][]> Signatures = new(StringComparer.OrdinalIgnoreCase)
    {
        [".png"] = [[0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]],
        [".jpg"] = [[0xFF, 0xD8, 0xFF]],
        [".jpeg"] = [[0xFF, 0xD8, 0xFF]],
        [".pdf"] = [[0x25, 0x50, 0x44, 0x46]],
        // DOCX/XLSX are ZIP containers.
        [".docx"] = [[0x50, 0x4B, 0x03, 0x04], [0x50, 0x4B, 0x05, 0x06]],
        [".xlsx"] = [[0x50, 0x4B, 0x03, 0x04], [0x50, 0x4B, 0x05, 0x06]]
    };

    public async Task<UploadResult> ValidateAsync(IFormFile file, CancellationToken ct = default)
    {
        if (file is null || file.Length == 0)
            return UploadResult.Rejected("File is empty");

        if (file.Length > _options.MaxFileSizeBytes)
            return UploadResult.Rejected("File exceeds the maximum permitted size");

        // Take the extension from the final segment only, and never trust the
        // client-supplied path. Path.GetFileName strips directory components that
        // a crafted multipart name may contain.
        var safeName = Path.GetFileName(file.FileName);
        var extension = Path.GetExtension(safeName);

        // Allowlist. A blocklist of dangerous extensions always loses: it has to
        // enumerate .php, .php5, .phtml, .asp, .aspx, .ashx, .jsp, .jspx and be
        // right every time, while the allowlist only has to name what you accept.
        if (string.IsNullOrEmpty(extension) || !_options.AllowedExtensions.Contains(extension))
        {
            _logger.LogWarning(
                "[T1505.003] Upload rejected. Technique={Technique} Extension={Extension} Reason={Reason}",
                "T1505.003", extension, "extension not in allowlist");
            return UploadResult.Rejected("File type is not permitted");
        }

        // Confirm the bytes agree with the extension, so shell.php renamed to
        // avatar.png is caught before it is written anywhere.
        await using var stream = file.OpenReadStream();
        if (!await MatchesSignatureAsync(stream, extension, ct))
        {
            _logger.LogWarning(
                "[T1505.003] Upload rejected. Technique={Technique} Extension={Extension} Reason={Reason}",
                "T1505.003", extension, "content does not match declared type");
            return UploadResult.Rejected("File content does not match its extension");
        }

        return UploadResult.Accepted(extension);
    }

    private static async Task<bool> MatchesSignatureAsync(Stream stream, string extension, CancellationToken ct)
    {
        if (!Signatures.TryGetValue(extension, out var candidates))
            return false; // Allowlisted types must have a signature to check.

        var longest = candidates.Max(c => c.Length);
        var header = new byte[longest];
        var read = await stream.ReadAtLeastAsync(header, longest, throwOnEndOfStream: false, ct);

        return candidates.Any(sig =>
            read >= sig.Length && header.AsSpan(0, sig.Length).SequenceEqual(sig));
    }

    /// <summary>
    /// Persist the upload so that it cannot be executed or served back as active content.
    /// This is the control that actually defeats T1505.003.
    /// </summary>
    public async Task<string> StoreAsync(IFormFile file, string extension, CancellationToken ct = default)
    {
        // Generate the stored name. Never reuse the client's filename on disk:
        // it carries traversal sequences, null bytes and double extensions.
        var storedName = $"{Guid.NewGuid():N}{extension}";

        // Outside the web root, so no route or static-file handler can reach it.
        // Best of all is object storage with no execution semantics at all.
        Directory.CreateDirectory(_options.StorageDirectory);
        var path = Path.Combine(_options.StorageDirectory, storedName);

        await using (var destination = new FileStream(path, FileMode.CreateNew))
        {
            await file.CopyToAsync(destination, ct);
        }

        // Remove execute permission. Defense in depth for the case where the
        // directory is later exposed by a misconfiguration.
        if (!OperatingSystem.IsWindows())
        {
            File.SetUnixFileMode(path,
                UnixFileMode.UserRead | UnixFileMode.UserWrite | UnixFileMode.GroupRead);
        }

        _logger.LogInformation("[T1505.003] Upload stored. StoredName={StoredName}", storedName);
        return storedName;
    }
}

[ApiController]
public class UploadController : ControllerBase
{
    private readonly UploadValidator _validator;

    public UploadController(UploadValidator validator) => _validator = validator;

    [HttpPost("api/uploads")]
    public async Task<IActionResult> Upload(IFormFile file, CancellationToken ct)
    {
        var result = await _validator.ValidateAsync(file, ct);
        if (!result.IsAccepted)
            return BadRequest(new { error = result.Reason });

        var storedName = await _validator.StoreAsync(file, result.Extension!, ct);
        return Ok(new { id = storedName });
    }

    /// <summary>
    /// Serve uploads back defensively. Content-Disposition: attachment plus
    /// X-Content-Type-Options: nosniff stops the browser from deciding that a
    /// stored file is HTML or script and running it in your origin.
    /// </summary>
    [HttpGet("api/uploads/{id}")]
    public IActionResult Download(string id)
    {
        if (!Guid.TryParseExact(Path.GetFileNameWithoutExtension(id), "N", out _))
            return NotFound();

        Response.Headers.XContentTypeOptions = "nosniff";
        Response.Headers.ContentSecurityPolicy = "default-src 'none'; sandbox";
        return PhysicalFile(Path.Combine("/var/uploads", Path.GetFileName(id)),
            "application/octet-stream", fileDownloadName: id);
    }
}

public class UploadOptions
{
    public long MaxFileSizeBytes { get; set; } = 10 * 1024 * 1024;

    /// <summary>Outside the web root. Object storage is better still.</summary>
    public string StorageDirectory { get; set; } = "/var/uploads";

    public HashSet<string> AllowedExtensions { get; set; } =
        new(StringComparer.OrdinalIgnoreCase) { ".png", ".jpg", ".jpeg", ".pdf", ".docx", ".xlsx" };
}

public record UploadResult
{
    public bool IsAccepted { get; init; }
    public string? Reason { get; init; }
    public string? Extension { get; init; }

    public static UploadResult Accepted(string extension) =>
        new() { IsAccepted = true, Extension = extension };

    public static UploadResult Rejected(string reason) =>
        new() { IsAccepted = false, Reason = reason };
}

/// <summary>
/// Key takeaways for T1505.003 (Web Shell):
///
/// 1. Store uploads outside the web root, ideally in object storage. If the file
///    cannot be executed, its contents stop mattering.
/// 2. Allowlist extensions; never try to enumerate the dangerous ones.
/// 3. Verify magic bytes so a renamed script is caught before it is written.
/// 4. Generate the stored filename yourself. Client names carry traversal
///    sequences, null bytes and double extensions.
/// 5. Remove execute permission on the stored file.
/// 6. Serve downloads with nosniff and Content-Disposition: attachment.
/// 7. For untrusted uploads, add a real malware scanner (Defender for Storage,
///    ClamAV, a vendor API). A string search for "eval(" is not one.
/// 8. Content signatures may support detection and triage, but they are not a
///    substitute for making the storage location non-executable.
///
/// References:
/// - MITRE ATT&CK T1505.003: https://attack.mitre.org/techniques/T1505/003/
/// - OWASP: File Upload Cheat Sheet
/// </summary>
