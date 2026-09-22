# MITRE ATT&CK for Developers — .NET/C# Code Samples

Educational samples demonstrating MITRE ATT&CK techniques and their defenses in
ASP.NET Core.

## ⚠️ Important notice

These samples are for **educational purposes only**. They pair vulnerable patterns
with their defended equivalents so both are recognisable. Do not ship the
vulnerable examples.

## Scope: what belongs in your code

Credential stuffing, password spraying, impossible travel, device reputation and
MFA belong to your **identity provider** — Microsoft Entra ID Protection sees
sign-ins across every application and tenant, and a single service cannot match
that context. Reimplementing those detections yields a weaker control that also
locks out legitimate roaming users.

Those techniques deserve **monitoring**, not reimplementation. These samples cover
what the platform cannot do for you.

## Overview

| File | ATT&CK Techniques | Description |
|------|------------------|-------------|
| `ResourceAuthorization.cs` | T1078 | Object-level and tenant authorization |
| `CommandInjection.cs` | T1059 | Command injection and safe process execution |
| `FileUploadValidation.cs` | T1505.003 | Upload handling that cannot be executed |
| `SessionSecurity.cs` | T1185, T1098, T1550.004 | Session rotation and revocation |
| `TamperEvidentLogger.cs` | T1070 | Hash-chained, tamper-evident audit log |
| `SecretsManagement.cs` | T1552 | Configuration providers and Key Vault |

## Sample details

### 1. ResourceAuthorization.cs — T1078

**The check no identity provider can make for you.** The IdP answers "is this a
real user with a valid token?" It cannot answer "may *this* user read *this*
record in *this* tenant," because only your application knows its object model.

```csharp
var doc = await _documents.FindAsync(id);
if (doc is null) return NotFound();

var result = await _authorization.AuthorizeAsync(User, doc, DocumentOperations.Read);
if (!result.Succeeded)
{
    _logger.LogWarning("[T1078] denied sub={Sub} doc={Doc}", subject, id);
    return NotFound();   // same shape as a miss, so 403 isn't an oracle
}
```

Key points:
- Load the resource **before** the decision. `[Authorize]` runs before model
  binding and cannot see the record, so object checks must be imperative.
- Return `404` on denial so the status code does not confirm the id exists.
- Make tenant isolation a hard boundary no role can override.
- Log denials with the technique id — one is noise, a hundred is enumeration.

### 2. CommandInjection.cs — T1059

Vulnerable shell concatenation versus `ArgumentList` with `UseShellExecute = false`,
plus host validation, an executable allowlist, and timeout enforcement.

```csharp
processInfo.ArgumentList.Add("-n");
processInfo.ArgumentList.Add("4");
processInfo.ArgumentList.Add(userInput);   // one argument, never a program
processInfo.UseShellExecute = false;
```

### 3. FileUploadValidation.cs — T1505.003

**Structural, not signature-based.** Scanning an upload for `eval(` or `<?php`
fails both ways: binary PDFs and images contain those byte sequences, while any
encoded payload passes. The durable control is making the storage location
non-executable.

```csharp
if (!_allowed.Contains(ext))                return Reject("type not permitted");
if (!await MatchesMagicBytesAsync(s, ext))  return Reject("content mismatch");

var stored = $"{Guid.NewGuid():N}{ext}";                  // you name it
var path = Path.Combine("/var/uploads", stored);          // outside web root
File.SetUnixFileMode(path, UserRead | UserWrite | GroupRead);   // no execute
```

Serve downloads with `X-Content-Type-Options: nosniff` and
`Content-Disposition: attachment`. For genuinely untrusted uploads, add a real
malware scanner — a string search is not one.

### 4. SessionSecurity.cs — T1185, T1098, T1550.004

Cryptographically random identifiers, rotation on privilege change to defeat
fixation, concurrent session limits, and server-side revocation.

A stolen cookie (T1550.004) bypasses MFA entirely, because the session is already
authenticated. That makes **revocation** more valuable than detecting how the
cookie was taken: keep session state you can delete, and delete it on password
change, privilege change, and reported compromise.

`EnforceIpBinding` is available but defaults to non-strict. Blocking on IP change
logs out mobile users who moved between towers while leaving an attacker on the
same network unaffected.

### 5. TamperEvidentLogger.cs — T1070

Each entry carries the hash of its predecessor, so modification, deletion and
reordering all break the chain detectably.

The honest limitation: a hash chain proves the local log **was** altered. It does
not prevent alteration, and an attacker with write access can rebuild the whole
chain unless the tip hash is anchored somewhere they do not control. Ship entries
to a SIEM or immutable storage; treat the chain as corroboration, not as the
primary control.

### 6. SecretsManagement.cs — T1552

Hardcoded credentials versus `IConfiguration` providers, User Secrets for local
development, Key Vault with `DefaultAzureCredential`, the Options pattern with
startup validation, and log sanitization.

```csharp
var client = new SecretClient(new Uri(vaultUri), new DefaultAzureCredential());
```

Prefer identity-based access directly to the downstream resource where it is
supported; a vault you still have to read a password out of is a smaller win than
not having a password at all.

## Requirements

- .NET 8.0 or later
- ASP.NET Core shared framework
- `Azure.Security.KeyVault.Secrets` and `Azure.Identity` for the Key Vault examples

## MITRE ATT&CK mapping

| Technique | Tactic | Sample File |
|-----------|--------|-------------|
| T1059 | Execution | `CommandInjection.cs` |
| T1070 | Defense Evasion | `TamperEvidentLogger.cs` |
| T1078 | Defense Evasion / Persistence | `ResourceAuthorization.cs` |
| T1098 | Persistence | `SessionSecurity.cs` |
| T1185 | Collection | `SessionSecurity.cs` |
| T1505.003 | Persistence | `FileUploadValidation.cs` |
| T1550.004 | Defense Evasion | `SessionSecurity.cs` |
| T1552 | Credential Access | `SecretsManagement.cs` |

### Configured, not coded

| Technique | Name | Where it belongs |
|-----------|------|------------------|
| T1110.003 | Password Spraying | Entra ID Protection / your IdP |
| T1110.004 | Credential Stuffing | Entra ID Protection / your IdP |
| T1552 | Unsecured Credentials *(detection)* | GitHub Secret Scanning + Push Protection |

## Production considerations

1. **Defense in depth** — no single control here is sufficient alone.
2. **Least privilege** — scope the workload identity to exactly what it reads.
3. **Shared state** — the in-memory dictionaries are for readability; real
   deployments need a distributed cache or database.
4. **Send events to a SIEM** — technique-tagged logs are only useful if something
   correlates them.
5. **Test the controls** — an authorization rule with no test is a rule that will
   regress.

## Learning resources

- [ATT&CK Framework](https://attack.mitre.org/) · [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) · [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [ASP.NET Core Security](https://learn.microsoft.com/aspnet/core/security/)
- [Resource-based authorization](https://learn.microsoft.com/aspnet/core/security/authorization/resourcebased)
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)
