using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Text;
using System.Text.RegularExpressions;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// Demonstrates defense against T1505.003 - Web Shell
/// Implements file upload validation and web shell detection
/// </summary>
public class WebShellDetection
{
    private readonly ILogger<WebShellDetection> _logger;
    private readonly WebShellDetectionOptions _options;

    // T1505.003: Known web shell signatures and patterns
    private static readonly string[] DangerousFileExtensions = 
    {
        ".php", ".php3", ".php4", ".php5", ".phtml",
        ".asp", ".aspx", ".asax", ".ascx", ".ashx", ".asmx", ".asa", ".cer",
        ".jsp", ".jspx",
        ".exe", ".dll", ".bat", ".cmd", ".ps1", ".sh",
        ".py", ".rb", ".pl", ".cgi"
    };

    // T1505.003: Web shell code signatures
    private static readonly string[] WebShellSignatures =
    {
        // PHP web shells
        "eval(", "base64_decode", "gzinflate", "system(", "exec(", "shell_exec",
        "passthru", "proc_open", "popen", "assert(", "preg_replace(.*\/e",
        "create_function", "include(", "require(", "$_GET", "$_POST", "$_REQUEST",
        "file_get_contents", "file_put_contents", "fwrite", "fputs",
        
        // ASP/ASPX web shells
        "eval(Request", "Execute(Request", "ExecuteGlobal", "Server.CreateObject",
        "WScript.Shell", "Shell.Application", "Process.Start",
        "System.Diagnostics.Process", "cmd.exe", "powershell.exe",
        
        // JSP web shells
        "Runtime.getRuntime", "ProcessBuilder", "exec(",
        
        // Generic suspicious patterns
        "backdoor", "c99", "r57", "webshell", "shell_exec", "cmd.exe",
        "powershell", "/bin/bash", "/bin/sh", "nc -", "netcat"
    };

    // T1505.003: Obfuscation patterns often used in web shells
    private static readonly Regex[] ObfuscationPatterns =
    {
        new Regex(@"chr\(\d+\)\s*\.", RegexOptions.IgnoreCase), // chr() concatenation
        new Regex(@"\\x[0-9a-f]{2}", RegexOptions.IgnoreCase), // hex encoding
        new Regex(@"\\[0-7]{3}", RegexOptions.IgnoreCase), // octal encoding
        new Regex(@"String\.fromCharCode", RegexOptions.IgnoreCase), // JavaScript obfuscation
        new Regex(@"eval\s*\(", RegexOptions.IgnoreCase), // eval usage
        new Regex(@"\$\{.*?\}", RegexOptions.IgnoreCase), // variable interpolation
        new Regex(@"base64_decode\s*\(", RegexOptions.IgnoreCase) // base64 obfuscation
    };

    // T1505.003: File header magic bytes for common types
    private static readonly Dictionary<string, byte[]> FileSignatures = new()
    {
        [".png"] = new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A },
        [".jpg"] = new byte[] { 0xFF, 0xD8, 0xFF },
        [".gif"] = new byte[] { 0x47, 0x49, 0x46, 0x38 },
        [".pdf"] = new byte[] { 0x25, 0x50, 0x44, 0x46 },
        [".zip"] = new byte[] { 0x50, 0x4B, 0x03, 0x04 },
        [".exe"] = new byte[] { 0x4D, 0x5A } // MZ header
    };

    public WebShellDetection(
        ILogger<WebShellDetection> logger,
        WebShellDetectionOptions? options = null)
    {
        _logger = logger;
        _options = options ?? new WebShellDetectionOptions();
    }

    /// <summary>
    /// T1505.003 Defense: Comprehensive file upload validation
    /// Validates file uploads to prevent web shell uploads
    /// </summary>
    [HttpPost("api/upload")]
    public async Task<IActionResult> ValidateAndUploadFileAsync(IFormFile file)
    {
        if (file == null || file.Length == 0)
        {
            return new BadRequestObjectResult(new { error = "No file uploaded" });
        }

        // Run all validation checks
        var validationResult = await ValidateUploadAsync(file);

        if (!validationResult.IsValid)
        {
            // T1505.003: Log suspicious upload attempt
            _logger.LogWarning(
                "[T1505.003] Suspicious file upload blocked: {FileName}, " +
                "Size: {Size}, ContentType: {ContentType}, Reason: {Reason}",
                file.FileName,
                file.Length,
                file.ContentType,
                validationResult.Reason);

            return new BadRequestObjectResult(new 
            { 
                error = "File validation failed",
                reason = validationResult.Reason,
                technique = "T1505.003 - Web Shell Upload Blocked"
            });
        }

        // File is validated, proceed with upload
        var savedPath = await SaveFileSecurelyAsync(file);

        _logger.LogInformation(
            "[T1505.003] File uploaded successfully: {FileName}, Path: {Path}",
            file.FileName,
            savedPath);

        return new OkObjectResult(new 
        { 
            success = true,
            fileName = file.FileName,
            path = savedPath
        });
    }

    /// <summary>
    /// T1505.003 Defense: Multi-layer file validation
    /// </summary>
    public async Task<ValidationResult> ValidateUploadAsync(IFormFile file)
    {
        // Defense Layer 1: File size validation
        if (file.Length > _options.MaxFileSizeBytes)
        {
            return ValidationResult.Failed(
                $"File size exceeds maximum allowed ({_options.MaxFileSizeBytes} bytes)");
        }

        if (file.Length == 0)
        {
            return ValidationResult.Failed("File is empty");
        }

        // Defense Layer 2: File extension validation (allowlist)
        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
        
        if (!_options.AllowedExtensions.Contains(extension))
        {
            return ValidationResult.Failed(
                $"File extension '{extension}' is not allowed");
        }

        // Defense Layer 3: Check for dangerous extensions
        if (DangerousFileExtensions.Contains(extension))
        {
            return ValidationResult.Failed(
                $"Dangerous file extension detected: {extension}");
        }

        // Defense Layer 4: Check for double extensions (e.g., image.jpg.php)
        if (HasDoubleExtension(file.FileName))
        {
            return ValidationResult.Failed(
                "Double extension detected (possible web shell technique)");
        }

        // Defense Layer 5: Content-Type validation
        if (!_options.AllowedContentTypes.Contains(file.ContentType.ToLowerInvariant()))
        {
            return ValidationResult.Failed(
                $"Content-Type '{file.ContentType}' is not allowed");
        }

        // Defense Layer 6: Validate file signature (magic bytes)
        using var stream = file.OpenReadStream();
        var signatureResult = await ValidateFileSignatureAsync(stream, extension);
        if (!signatureResult.IsValid)
        {
            return signatureResult;
        }

        // Defense Layer 7: Scan content for web shell signatures
        stream.Position = 0;
        var contentResult = await ScanFileContentAsync(stream, file.FileName);
        if (!contentResult.IsValid)
        {
            return contentResult;
        }

        // Defense Layer 8: Check for suspicious file names
        var fileNameResult = ValidateFileName(file.FileName);
        if (!fileNameResult.IsValid)
        {
            return fileNameResult;
        }

        return ValidationResult.Success();
    }

    /// <summary>
    /// T1505.003 Defense: Validate file magic bytes match claimed extension
    /// </summary>
    private async Task<ValidationResult> ValidateFileSignatureAsync(Stream stream, string extension)
    {
        if (!FileSignatures.TryGetValue(extension, out var expectedSignature))
        {
            // No signature check available for this extension
            return ValidationResult.Success();
        }

        var buffer = new byte[expectedSignature.Length];
        var bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);

        if (bytesRead < expectedSignature.Length)
        {
            return ValidationResult.Failed(
                "File is too small to verify signature");
        }

        // Check if file signature matches expected
        for (int i = 0; i < expectedSignature.Length; i++)
        {
            if (buffer[i] != expectedSignature[i])
            {
                return ValidationResult.Failed(
                    $"File signature mismatch. File claims to be {extension} but header doesn't match. " +
                    "Possible renamed web shell.");
            }
        }

        return ValidationResult.Success();
    }

    /// <summary>
    /// T1505.003 Defense: Scan file content for web shell signatures
    /// </summary>
    private async Task<ValidationResult> ScanFileContentAsync(Stream stream, string fileName)
    {
        // Read file content (limit to prevent memory issues)
        var maxBytesToScan = Math.Min(stream.Length, _options.MaxContentScanBytes);
        var buffer = new byte[maxBytesToScan];
        await stream.ReadAsync(buffer, 0, (int)maxBytesToScan);

        // Convert to string for pattern matching
        var content = Encoding.UTF8.GetString(buffer);
        var contentLower = content.ToLowerInvariant();

        // Check for web shell signatures
        foreach (var signature in WebShellSignatures)
        {
            if (contentLower.Contains(signature.ToLowerInvariant()))
            {
                _logger.LogWarning(
                    "[T1505.003] SECURITY ALERT: Web shell signature detected in {FileName}: '{Signature}'",
                    fileName,
                    signature);

                return ValidationResult.Failed(
                    $"Suspicious content detected. File contains potential web shell code.");
            }
        }

        // Check for obfuscation patterns
        foreach (var pattern in ObfuscationPatterns)
        {
            if (pattern.IsMatch(content))
            {
                _logger.LogWarning(
                    "[T1505.003] SECURITY ALERT: Obfuscation pattern detected in {FileName}: {Pattern}",
                    fileName,
                    pattern.ToString());

                return ValidationResult.Failed(
                    "Suspicious obfuscation patterns detected");
            }
        }

        // Check for excessive special characters (possible obfuscation)
        var specialCharCount = content.Count(c => !char.IsLetterOrDigit(c) && !char.IsWhiteSpace(c));
        var specialCharRatio = (double)specialCharCount / content.Length;

        if (specialCharRatio > 0.3) // More than 30% special characters
        {
            _logger.LogWarning(
                "[T1505.003] SECURITY ALERT: High special character ratio in {FileName}: {Ratio:P}",
                fileName,
                specialCharRatio);

            return ValidationResult.Failed(
                "File contains suspicious amount of special characters (possible obfuscation)");
        }

        return ValidationResult.Success();
    }

    /// <summary>
    /// T1505.003 Defense: Validate file name for suspicious patterns
    /// </summary>
    private ValidationResult ValidateFileName(string fileName)
    {
        var fileNameLower = fileName.ToLowerInvariant();

        // Check for path traversal attempts
        if (fileName.Contains("..") || fileName.Contains("/") || fileName.Contains("\\"))
        {
            return ValidationResult.Failed(
                "File name contains path traversal characters");
        }

        // Check for null bytes (can bypass extension filters)
        if (fileName.Contains('\0'))
        {
            return ValidationResult.Failed(
                "File name contains null bytes (possible evasion technique)");
        }

        // Check for suspicious keywords in file name
        var suspiciousKeywords = new[] 
        { 
            "shell", "backdoor", "webshell", "cmd", "exec", "eval",
            "c99", "r57", "b374k", "wso", "bypass"
        };

        foreach (var keyword in suspiciousKeywords)
        {
            if (fileNameLower.Contains(keyword))
            {
                return ValidationResult.Failed(
                    $"File name contains suspicious keyword: {keyword}");
            }
        }

        // Validate file name length
        if (fileName.Length > 255)
        {
            return ValidationResult.Failed(
                "File name exceeds maximum length");
        }

        return ValidationResult.Success();
    }

    /// <summary>
    /// T1505.003 Defense: Check for double extensions
    /// Attackers may use names like "image.jpg.php" to bypass filters
    /// </summary>
    private bool HasDoubleExtension(string fileName)
    {
        var parts = fileName.Split('.');
        
        // If more than 2 parts (name + 2+ extensions), it's suspicious
        if (parts.Length > 2)
        {
            // Check if any of the extensions (except the last one) is dangerous
            for (int i = 1; i < parts.Length - 1; i++)
            {
                var ext = "." + parts[i].ToLowerInvariant();
                if (DangerousFileExtensions.Contains(ext))
                {
                    return true;
                }
            }
        }

        return false;
    }

    /// <summary>
    /// T1505.003 Defense: Save file securely with renamed filename
    /// </summary>
    private async Task<string> SaveFileSecurelyAsync(IFormFile file)
    {
        // Generate random filename to prevent direct access/execution
        var randomFileName = $"{Guid.NewGuid()}{Path.GetExtension(file.FileName)}";
        
        // Store outside web root if possible
        var uploadPath = Path.Combine(_options.UploadDirectory, randomFileName);
        
        // Ensure upload directory exists
        Directory.CreateDirectory(_options.UploadDirectory);

        using var stream = new FileStream(uploadPath, FileMode.Create);
        await file.CopyToAsync(stream);

        // Set restrictive file permissions (if on Unix)
        if (OperatingSystem.IsLinux() || OperatingSystem.IsMacOS())
        {
            // Remove execute permissions: chmod 644
            File.SetUnixFileMode(uploadPath, 
                UnixFileMode.UserRead | UnixFileMode.UserWrite | 
                UnixFileMode.GroupRead | UnixFileMode.OtherRead);
        }

        return uploadPath;
    }

    /// <summary>
    /// T1505.003 Detection: Scan existing files for web shells
    /// Use this to periodically scan upload directories
    /// </summary>
    public async Task<List<SuspiciousFileReport>> ScanDirectoryForWebShellsAsync(string directoryPath)
    {
        var suspiciousFiles = new List<SuspiciousFileReport>();

        if (!Directory.Exists(directoryPath))
        {
            return suspiciousFiles;
        }

        var files = Directory.GetFiles(directoryPath, "*.*", SearchOption.AllDirectories);

        foreach (var filePath in files)
        {
            try
            {
                var fileInfo = new FileInfo(filePath);
                var extension = fileInfo.Extension.ToLowerInvariant();

                // Check for dangerous extensions
                if (DangerousFileExtensions.Contains(extension))
                {
                    suspiciousFiles.Add(new SuspiciousFileReport
                    {
                        FilePath = filePath,
                        Reason = $"Dangerous file extension: {extension}",
                        Severity = "HIGH"
                    });
                    continue;
                }

                // Scan file content
                using var stream = File.OpenRead(filePath);
                var contentResult = await ScanFileContentAsync(stream, filePath);
                
                if (!contentResult.IsValid)
                {
                    suspiciousFiles.Add(new SuspiciousFileReport
                    {
                        FilePath = filePath,
                        Reason = contentResult.Reason ?? "Suspicious content detected",
                        Severity = "CRITICAL"
                    });
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, 
                    "[T1505.003] Error scanning file {FilePath}", 
                    filePath);
            }
        }

        if (suspiciousFiles.Any())
        {
            _logger.LogWarning(
                "[T1505.003] SECURITY ALERT: Found {Count} suspicious files in {Directory}",
                suspiciousFiles.Count,
                directoryPath);
        }

        return suspiciousFiles;
    }
}

#region Supporting Types

public class ValidationResult
{
    public bool IsValid { get; init; }
    public string? Reason { get; init; }

    public static ValidationResult Success() => new() { IsValid = true };
    public static ValidationResult Failed(string reason) => new() { IsValid = false, Reason = reason };
}

public class WebShellDetectionOptions
{
    public long MaxFileSizeBytes { get; set; } = 10 * 1024 * 1024; // 10 MB
    public long MaxContentScanBytes { get; set; } = 5 * 1024 * 1024; // 5 MB
    public string UploadDirectory { get; set; } = "/var/uploads"; // Outside web root!
    
    public HashSet<string> AllowedExtensions { get; set; } = new(StringComparer.OrdinalIgnoreCase)
    {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".txt", ".csv", ".zip"
    };

    public HashSet<string> AllowedContentTypes { get; set; } = new(StringComparer.OrdinalIgnoreCase)
    {
        "image/jpeg", "image/png", "image/gif", "image/bmp",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain", "text/csv",
        "application/zip"
    };
}

public class SuspiciousFileReport
{
    public required string FilePath { get; init; }
    public required string Reason { get; init; }
    public required string Severity { get; init; }
    public DateTime DetectedAt { get; init; } = DateTime.UtcNow;
}

#endregion

/// <summary>
/// Key Takeaways for T1505.003 Defense (Web Shell):
/// 
/// Prevention:
/// 1. Use extension allowlist (not blocklist)
/// 2. Validate Content-Type headers
/// 3. Verify file signatures (magic bytes)
/// 4. Scan content for web shell signatures
/// 5. Check for double extensions
/// 6. Rename uploaded files to prevent execution
/// 7. Store uploads outside web root
/// 8. Remove execute permissions on uploaded files
/// 9. Validate file names for path traversal
/// 10. Enforce file size limits
/// 
/// Detection:
/// 1. Regularly scan upload directories
/// 2. Monitor for suspicious file access patterns
/// 3. Check for files with dangerous extensions
/// 4. Look for obfuscation patterns
/// 5. Monitor file creation in unexpected directories
/// 6. Alert on files with high entropy (possible encryption)
/// 7. Track file modifications in static content directories
/// 8. Monitor for web shell network indicators (reverse shells, C2)
/// 
/// Response:
/// 1. Quarantine suspicious files immediately
/// 2. Block source IP addresses
/// 3. Invalidate user sessions
/// 4. Review access logs for compromise indicators
/// 5. Check for persistence mechanisms
/// 6. Scan for lateral movement
/// 7. Restore from known-good backups
/// 8. Conduct forensic analysis
/// 
/// Additional Defenses:
/// - Implement Web Application Firewall (WAF)
/// - Use file integrity monitoring (FIM)
/// - Deploy endpoint detection and response (EDR)
/// - Enable application allowlisting
/// - Implement least privilege for web server processes
/// - Use read-only file systems where possible
/// - Enable security headers (X-Content-Type-Options: nosniff)
/// - Disable script execution in upload directories (web.config, .htaccess)
/// 
/// References:
/// - MITRE ATT&CK T1505.003: https://attack.mitre.org/techniques/T1505/003/
/// - OWASP: Unrestricted File Upload
/// - NSA: Detecting Web Shells
/// - SANS: Web Shell Detection
/// </summary>
