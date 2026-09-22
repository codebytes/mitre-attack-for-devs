using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authorization.Infrastructure;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace MitreAttackForDevs.Samples;

/// <summary>
/// T1078 (Valid Accounts) and T1530/T1213 (data collection) at the layer the
/// identity provider cannot reach.
///
/// The IdP answers "is this a real user, and is the token good?" It cannot answer
/// "may THIS user read THIS record in THIS tenant?" Only the application knows its
/// own object model, so object-level and tenant-level authorization is application code.
///
/// Reference: https://attack.mitre.org/techniques/T1078/
/// </summary>
public static class DocumentOperations
{
    public static readonly OperationAuthorizationRequirement Read = new() { Name = nameof(Read) };
    public static readonly OperationAuthorizationRequirement Update = new() { Name = nameof(Update) };
    public static readonly OperationAuthorizationRequirement Export = new() { Name = nameof(Export) };
}

public record Document
{
    public required Guid Id { get; init; }
    public required string TenantId { get; init; }
    public required string OwnerId { get; init; }
    public required string Classification { get; init; } // "public" | "internal" | "restricted"
}

/// <summary>
/// VULNERABLE: authenticated is treated as authorized.
///
/// The token is valid, the signature checks out, and the IdP is perfectly configured.
/// The attacker simply asks for a different id. This is an insecure direct object
/// reference, and no amount of identity hardening fixes it.
/// </summary>
[ApiController]
public class VulnerableDocumentController : ControllerBase
{
    private readonly IDocumentRepository _documents;

    public VulnerableDocumentController(IDocumentRepository documents) => _documents = documents;

    [Authorize] // Proves who they are. Says nothing about which documents they may read.
    [HttpGet("api/vulnerable/documents/{id}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var document = await _documents.FindAsync(id);
        if (document is null)
            return NotFound();

        // No tenant check, no owner check, no classification check.
        return Ok(document);
    }
}

/// <summary>
/// DEFENDED: every read resolves the object first, then authorizes the caller
/// against that specific object.
/// </summary>
[ApiController]
public class SecureDocumentController : ControllerBase
{
    private readonly IDocumentRepository _documents;
    private readonly IAuthorizationService _authorization;
    private readonly ILogger<SecureDocumentController> _logger;

    public SecureDocumentController(
        IDocumentRepository documents,
        IAuthorizationService authorization,
        ILogger<SecureDocumentController> logger)
    {
        _documents = documents;
        _authorization = authorization;
        _logger = logger;
    }

    [Authorize]
    [HttpGet("api/documents/{id}")]
    public async Task<IActionResult> Get(Guid id)
    {
        var document = await _documents.FindAsync(id);
        if (document is null)
            return NotFound();

        var result = await _authorization.AuthorizeAsync(User, document, DocumentOperations.Read);
        if (!result.Succeeded)
        {
            // Emit the denial with the ATT&CK id so the SIEM can correlate a caller
            // who is probing many ids. A single 403 is noise; a hundred is an attack.
            _logger.LogWarning(
                "[T1078] Authorization denied. Technique={Technique} Subject={Subject} Document={DocumentId} Operation={Operation}",
                "T1078", User.FindFirstValue(ClaimTypes.NameIdentifier), id, DocumentOperations.Read.Name);

            // Return the same shape as a miss so the response does not confirm existence.
            return NotFound();
        }

        return Ok(document);
    }
}

/// <summary>
/// Authorization handler carrying the rules only the application knows.
/// Tenant isolation is checked first and is never overridable by a role.
/// </summary>
public class DocumentAuthorizationHandler
    : AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        var tenantId = context.User.FindFirstValue("tid");
        var subjectId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);

        // Tenant isolation is a hard boundary. A global admin in tenant A is still
        // not a user of tenant B. Fail before any role is considered.
        if (string.IsNullOrEmpty(tenantId) || tenantId != resource.TenantId)
            return Task.CompletedTask;

        var isOwner = subjectId is not null && subjectId == resource.OwnerId;

        if (requirement.Name == DocumentOperations.Read.Name)
        {
            if (isOwner || resource.Classification != "restricted" || context.User.IsInRole("Compliance"))
                context.Succeed(requirement);
        }
        else if (requirement.Name == DocumentOperations.Update.Name)
        {
            if (isOwner || context.User.IsInRole("Editor"))
                context.Succeed(requirement);
        }
        else if (requirement.Name == DocumentOperations.Export.Name)
        {
            // Bulk export of restricted data requires a recently proven credential,
            // not merely a valid session. The IdP issues the acr/amr claim; the
            // application decides which operations demand it.
            var hasStepUp = context.User.HasClaim("acr", "mfa");
            if (context.User.IsInRole("Compliance") && (resource.Classification != "restricted" || hasStepUp))
                context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}

public interface IDocumentRepository
{
    Task<Document?> FindAsync(Guid id);
}

/// <summary>
/// Registration:
///
///   builder.Services.AddAuthorizationBuilder()
///       .AddPolicy("SameTenant", p => p.RequireClaim("tid"));
///   builder.Services.AddSingleton&lt;IAuthorizationHandler, DocumentAuthorizationHandler&gt;();
///
/// Key points for T1078 defense:
/// 1. Authentication is not authorization. Check the object, not just the token.
/// 2. Resolve the resource, then authorize against it. Attribute-only checks run
///    before model binding and cannot see the record.
/// 3. Make tenant isolation a hard boundary that no role can override.
/// 4. Log denials with the technique id so repeated probing is visible to the SIEM.
/// 5. Require step-up (acr/amr) for high-impact operations. The IdP proves it;
///    the application decides where it is required.
/// </summary>
