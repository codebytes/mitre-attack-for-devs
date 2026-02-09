# MITRE ATT&CK for Developers - Quick Reference

## Files Created

1. **CommandInjection.cs** (10KB) - T1059
2. **SessionSecurity.cs** (17KB) - T1185, T1098, T1550.004
3. **TamperEvidentLogger.cs** (17KB) - T1070
4. **SecretsManagement.cs** (22KB) - T1552
5. **WebShellDetection.cs** (20KB) - T1505.003

Total: ~86KB of educational security code samples

## Quick Reference: Defensive Patterns

### Command Injection (T1059)
```csharp
// ❌ NEVER: shell execution with user input
Arguments = $"-c \"ping {userInput}\""

// ✅ ALWAYS: ArgumentList with no shell
processInfo.ArgumentList.Add("-c");
processInfo.ArgumentList.Add("4");
processInfo.ArgumentList.Add(userInput);
processInfo.UseShellExecute = false;
```

### Session Security (T1185, T1098)
```csharp
// ✅ Fingerprint binding
var fingerprint = SHA256(ip + userAgent);

// ✅ Rotate on privilege change
await RotateSessionOnPrivilegeChangeAsync(oldSessionId, "admin", context);

// ✅ Detect concurrent sessions
if (activeSessions > maxConcurrentSessions)
    await AlertSecurityTeam();
```

### Tamper-Evident Logging (T1070)
```csharp
// ✅ Hash chain (blockchain-like)
entry.PreviousHash = lastHash;
entry.Hash = SHA256(entry.Data + entry.PreviousHash);

// ✅ Verification
var result = logger.VerifyLogIntegrity();
if (!result.IsValid)
    Alert($"Tampering detected: {result.Message}");
```

### Secrets Management (T1552)
```csharp
// ❌ NEVER: hardcode secrets
private const string ApiKey = "sk_live_1234...";

// ✅ ALWAYS: secure configuration
var apiKey = _configuration["ApiKeys:Stripe"];

// ✅ Azure Key Vault
var client = new SecretClient(vaultUri, new DefaultAzureCredential());
var secret = await client.GetSecretAsync("ApiKey");
```

### Web Shell Detection (T1505.003)
```csharp
// ✅ Extension allowlist
if (!allowedExtensions.Contains(extension))
    return ValidationResult.Failed();

// ✅ Magic bytes verification
if (fileHeader != expectedSignature)
    return ValidationResult.Failed("Signature mismatch");

// ✅ Content scanning
if (content.Contains("eval(") || content.Contains("shell_exec"))
    return ValidationResult.Failed("Web shell detected");

// ✅ Secure storage
var randomName = $"{Guid.NewGuid()}{extension}";
File.SetUnixFileMode(path, UserRead | UserWrite);
```

## ATT&CK Technique Coverage

| ID | Name | Tactic | File |
|----|------|--------|------|
| T1059 | Command and Scripting Interpreter | Execution | CommandInjection.cs |
| T1070 | Indicator Removal | Defense Evasion | TamperEvidentLogger.cs |
| T1098 | Account Manipulation | Persistence | SessionSecurity.cs |
| T1185 | Browser Session Hijacking | Collection | SessionSecurity.cs |
| T1505.003 | Web Shell | Persistence | WebShellDetection.cs |
| T1550.004 | Web Session Cookie | Defense Evasion | SessionSecurity.cs |
| T1552 | Unsecured Credentials | Credential Access | SecretsManagement.cs |

## Conference Talk Flow (Suggested)

### Part 1: Execution & Command Injection (5 min)
- Show vulnerable ping endpoint
- Live demo: `"google.com && whoami"`
- Show defended version
- Key takeaway: **Never use shell execution**

### Part 2: Credential Access (5 min)
- Show hardcoded secrets examples
- Explain git history exposure
- Show secure patterns (User Secrets, Key Vault)
- Key takeaway: **Configuration, not code**

### Part 3: Persistence & Web Shells (5 min)
- Show file upload without validation
- Demo web shell upload attempt
- Show multi-layer validation
- Key takeaway: **Defense in depth**

### Part 4: Defense Evasion (5 min)
- Show log tampering attempt
- Explain hash chain concept
- Demo tamper detection
- Key takeaway: **Verify, don't trust**

### Part 5: Session Security (5 min)
- Explain session hijacking
- Show fingerprinting and rotation
- Demo concurrent session detection
- Key takeaway: **Bind sessions to clients**

## Demo Commands

```bash
# Command Injection Demo
curl "http://localhost:5000/api/vulnerable/ping?host=google.com%20%26%26%20whoami"
curl "http://localhost:5000/api/secure/ping?host=google.com"

# Web Shell Upload Demo
curl -X POST -F "file=@webshell.php" http://localhost:5000/api/upload

# Log Tampering Demo
# 1. Write entries
# 2. Manually edit log file
# 3. Run verification
# 4. Show tamper detection

# Secrets in Git Demo
git log -p | grep -i "password"
git log -p | grep -i "api.*key"
```

## Key Messages

1. **Know Your Enemy** - Understand ATT&CK techniques
2. **Security by Design** - Not an afterthought
3. **Defense in Depth** - Multiple layers
4. **Verify, Don't Trust** - Validate everything
5. **Fail Securely** - Safe defaults

## Resources for Attendees

- 📁 Code samples: `/samples/dotnet/`
- 📖 README with detailed explanations
- 🔗 MITRE ATT&CK links in comments
- 🔗 OWASP references
- 🔗 Microsoft security docs

## Next Steps for Attendees

1. ✅ Clone the samples repository
2. ✅ Review each file (vulnerable → defended)
3. ✅ Run the example usage sections
4. ✅ Adapt patterns for your projects
5. ✅ Add to your security checklist
6. ✅ Share with your team
7. ✅ Integrate into code reviews

## Questions to Anticipate

**Q: Are these production-ready?**
A: They're educational samples. Extract patterns and adapt for your needs.

**Q: What about other languages?**
A: Principles apply universally. Look for similar patterns in Python, Java, etc.

**Q: How do I test these?**
A: Each file has example usage. Create test project and run the demos.

**Q: What's the performance impact?**
A: Security controls have minimal impact. Session fingerprinting and hash chains are fast.

**Q: What about false positives?**
A: Web shell detection may flag legitimate code. Tune signatures for your environment.

---

**Presenter Notes:**
- Emphasize these are **educational** - show both bad and good
- Live demos are powerful - have them ready
- Focus on **patterns**, not just code
- Connect to real-world breaches
- End with actionable takeaways
