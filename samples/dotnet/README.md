# MITRE ATT&CK for Developers - .NET/C# Code Samples

Educational code samples demonstrating common MITRE ATT&CK techniques and their defenses in .NET/C#.

## ⚠️ Important Notice

These samples are for **educational purposes only**. They demonstrate both vulnerable and secure coding patterns to teach developers about security threats and defenses. Do not use the vulnerable examples in production code.

## Overview

This collection contains 5 comprehensive code samples covering critical MITRE ATT&CK techniques:

| File | ATT&CK Techniques | Description |
|------|------------------|-------------|
| `CommandInjection.cs` | T1059 | Command injection vulnerabilities and defenses |
| `SessionSecurity.cs` | T1185, T1098, T1550.004 | Secure session management with fingerprinting |
| `TamperEvidentLogger.cs` | T1070 | Tamper-evident logging using hash chains |
| `SecretsManagement.cs` | T1552 | Secure secrets management patterns |
| `WebShellDetection.cs` | T1505.003 | Web shell detection and file upload validation |

## Sample Details

### 1. CommandInjection.cs - T1059

**Technique:** Command and Scripting Interpreter

**What it demonstrates:**
- ❌ Vulnerable patterns with shell command injection
- ✅ Safe process execution without shell interpretation
- ✅ Input validation with allowlists
- ✅ Argument separation to prevent injection
- ✅ Timeout enforcement and logging

**Key defensive patterns:**
```csharp
// Use ArgumentList instead of Arguments string
processInfo.ArgumentList.Add("-n");
processInfo.ArgumentList.Add("4");
processInfo.ArgumentList.Add(userInput); // Safe - treated as single argument

// Never use shell execution
UseShellExecute = false
```

### 2. SessionSecurity.cs - T1185, T1098, T1550.004

**Techniques:** 
- T1185: Browser Session Hijacking
- T1098: Account Manipulation
- T1550.004: Web Session Cookie

**What it demonstrates:**
- ✅ Session fingerprinting (IP + User-Agent hash)
- ✅ Session rotation on privilege changes
- ✅ Concurrent session detection and limits
- ✅ Automatic session invalidation on suspicious activity
- ✅ Cryptographically secure session IDs

**Key defensive patterns:**
```csharp
// Bind session to client characteristics
var fingerprint = GenerateClientFingerprint(httpContext);

// Rotate on privilege escalation (prevents session fixation)
await RotateSessionOnPrivilegeChangeAsync(sessionId, "admin", httpContext);

// Detect anomalies
await DetectConcurrentSessionAnomaliesAsync(userId, session);
```

### 3. TamperEvidentLogger.cs - T1070

**Technique:** Indicator Removal on Host

**What it demonstrates:**
- ✅ Hash chain logging (blockchain-like structure)
- ✅ Tamper detection through hash verification
- ✅ Sequence number validation
- ✅ Cryptographic proof of log integrity
- ✅ Security event correlation with ATT&CK IDs

**Key defensive patterns:**
```csharp
// Each entry includes hash of previous entry
entry.PreviousHash = _lastHash;
entry.Hash = ComputeEntryHash(entry);

// Verification detects any tampering
var result = logger.VerifyLogIntegrity();
if (!result.IsValid)
    Alert($"T1070 DETECTED: {result.Message}");
```

### 4. SecretsManagement.cs - T1552

**Technique:** Unsecured Credentials

**What it demonstrates:**
- ❌ Hardcoded credentials (what NOT to do)
- ❌ Secrets in configuration files
- ✅ IConfiguration with secure providers
- ✅ User Secrets for development
- ✅ Azure Key Vault integration
- ✅ Options pattern with validation
- ✅ Safe error handling and logging

**Key defensive patterns:**
```csharp
// Use configuration providers (no hardcoded secrets)
var apiKey = _configuration["ApiKeys:Stripe"];

// Azure Key Vault with Managed Identity
var client = new SecretClient(
    new Uri(keyVaultUrl), 
    new DefaultAzureCredential());

// Sanitize logs
var masked = $"****{apiKey.Substring(apiKey.Length - 4)}";
```

### 5. WebShellDetection.cs - T1505.003

**Technique:** Server Software Component: Web Shell

**What it demonstrates:**
- ✅ Multi-layer file upload validation
- ✅ Extension allowlist (not blocklist)
- ✅ File signature verification (magic bytes)
- ✅ Content scanning for web shell signatures
- ✅ Obfuscation pattern detection
- ✅ Double extension detection
- ✅ Secure file storage (renamed, outside web root)

**Key defensive patterns:**
```csharp
// Validate file signature matches extension
var signatureResult = await ValidateFileSignatureAsync(stream, extension);

// Scan content for web shell patterns
if (content.Contains("eval(") || content.Contains("shell_exec"))
    return ValidationResult.Failed("Web shell detected");

// Rename and store securely
var randomFileName = $"{Guid.NewGuid()}{extension}";
File.SetUnixFileMode(path, UserRead | UserWrite | GroupRead | OtherRead);
```

## Requirements

- .NET 8.0 or later
- ASP.NET Core packages (for HTTP examples)
- Azure.Security.KeyVault.Secrets (for Key Vault examples)
- Azure.Identity (for Managed Identity)

## Usage

These are **educational samples**, not production libraries. To use them:

1. **Review the code** - Read both vulnerable and defended examples
2. **Understand the patterns** - Each file has detailed comments
3. **Adapt for your needs** - Extract the defensive patterns you need
4. **Test thoroughly** - Always test security controls

### Example: Integrating Secure Session Management

```csharp
// In Program.cs or Startup.cs
builder.Services.AddSingleton<SecureSessionManager>();
builder.Services.Configure<SessionSecurityOptions>(options =>
{
    options.SessionTimeout = TimeSpan.FromMinutes(30);
    options.MaxConcurrentSessions = 3;
    options.EnforceIpBinding = true;
});

// In your controller
private readonly SecureSessionManager _sessionManager;

public async Task<IActionResult> Login(LoginModel model)
{
    if (await ValidateCredentials(model))
    {
        var session = await _sessionManager.CreateSessionAsync(
            model.UserId, 
            HttpContext);
            
        Response.Cookies.Append("SessionId", session.SessionId, new CookieOptions
        {
            HttpOnly = true,
            Secure = true,
            SameSite = SameSiteMode.Strict
        });
        
        return Ok();
    }
    return Unauthorized();
}
```

### Example: Using Tamper-Evident Logger

```csharp
var logger = new TamperEvidentLogger("/var/log/security-audit.log");

// Log security events with ATT&CK technique IDs
await logger.WriteSecurityEventAsync(
    technique: "T1059",
    description: "Blocked command injection attempt",
    severity: "HIGH",
    userId: userId,
    details: new Dictionary<string, object>
    {
        ["Command"] = suspiciousInput,
        ["SourceIP"] = ipAddress
    });

// Verify integrity periodically
var verification = logger.VerifyLogIntegrity();
if (!verification.IsValid)
{
    // Alert security team
    await NotifySecurityTeam($"Log tampering detected: {verification.Message}");
}
```

## Testing the Samples

Each file includes example usage. To test:

```bash
# Create a test project
dotnet new console -n MitreAttackTests
cd MitreAttackTests

# Copy sample files
cp ../CommandInjection.cs .
cp ../SessionSecurity.cs .
# ... etc

# Add required packages
dotnet add package Microsoft.AspNetCore.App
dotnet add package Azure.Security.KeyVault.Secrets
dotnet add package Azure.Identity

# Create a test program
# See individual files for example usage sections
```

## Security Considerations

### For Production Use

When adapting these patterns for production:

1. **Defense in Depth** - Use multiple security layers
2. **Principle of Least Privilege** - Minimize permissions
3. **Secure Defaults** - Start with most restrictive settings
4. **Logging and Monitoring** - Log security events to SIEM
5. **Regular Updates** - Keep dependencies updated
6. **Security Testing** - Include in CI/CD pipeline
7. **Incident Response** - Have procedures for detected attacks

### Additional Protections

- **Web Application Firewall (WAF)** - CloudFlare, Azure WAF, AWS WAF
- **Runtime Application Self-Protection (RASP)** - Contrast, Sqreen
- **Static Analysis** - SonarQube, Checkmarx, Veracode
- **Dependency Scanning** - Dependabot, Snyk, OWASP Dependency-Check
- **Secret Scanning** - GitGuardian, TruffleHog, git-secrets

## MITRE ATT&CK Mapping

| Technique | Tactic | Sample File |
|-----------|--------|-------------|
| T1059 | Execution | CommandInjection.cs |
| T1070 | Defense Evasion | TamperEvidentLogger.cs |
| T1098 | Persistence | SessionSecurity.cs |
| T1185 | Collection | SessionSecurity.cs |
| T1505.003 | Persistence | WebShellDetection.cs |
| T1550.004 | Defense Evasion | SessionSecurity.cs |
| T1552 | Credential Access | SecretsManagement.cs |

## Learning Resources

### MITRE ATT&CK
- [ATT&CK Framework](https://attack.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)

### Secure Coding
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [Microsoft Security Development Lifecycle](https://www.microsoft.com/securityengineering/sdl)

### .NET Security
- [ASP.NET Core Security](https://docs.microsoft.com/aspnet/core/security/)
- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/)
- [.NET Security Guidelines](https://docs.microsoft.com/dotnet/standard/security/)

## Contributing

These samples are for educational use. If you find issues or want to suggest improvements:

1. Ensure changes enhance educational value
2. Maintain both vulnerable and defended examples
3. Include detailed comments and ATT&CK technique IDs
4. Test all code patterns
5. Update documentation

## License

These educational samples are provided as-is for learning purposes. Adapt and modify as needed for your security training and development needs.

## Acknowledgments

- MITRE Corporation for the ATT&CK framework
- OWASP for security guidance and resources
- The .NET security community

---

**Remember:** Security is a continuous process, not a destination. Stay informed about new threats and continuously improve your security posture.

**Disclaimer:** These samples demonstrate security concepts for educational purposes. The vulnerable examples are intentionally insecure to illustrate attack patterns. Never use vulnerable patterns in production code.
