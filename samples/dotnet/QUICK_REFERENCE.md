# MITRE ATT&CK for Developers — Quick Reference

## Division of labour

| Configure in your identity provider | Write in your application |
|---|---|
| Credential stuffing, password spray (T1110) | Object + tenant authorization (T1078) |
| Impossible travel, device reputation | Export limits on your data (T1213, T1567) |
| MFA, step-up, passwordless | Input boundaries to interpreters (T1059, T1190) |
| Token issuance, refresh, revocation | Upload handling (T1505.003) |
| Cross-application sign-in risk | Business-meaningful audit events (T1070) |

A homegrown copy of an IdP feature is strictly worse than the product you already
pay for, and it locks out real users. Spend the effort on the right column.

## Defensive patterns

### Object authorization (T1078)
```csharp
// ❌ Authenticated is not authorized. The token is valid; the record isn't theirs.
[Authorize] public IActionResult Get(Guid id) => Ok(_repo.Find(id));

// ✅ Resolve the resource, then authorize against it
var doc = await _repo.FindAsync(id);
if (doc is null) return NotFound();
var ok = await _authz.AuthorizeAsync(User, doc, Operations.Read);
if (!ok.Succeeded) return NotFound();   // 404, so the status isn't an oracle
```

### Command injection (T1059)
```csharp
// ❌ NEVER: shell execution with user input
Arguments = $"-c \"ping {userInput}\""

// ✅ ALWAYS: ArgumentList, no shell
processInfo.ArgumentList.Add("-c");
processInfo.ArgumentList.Add("4");
processInfo.ArgumentList.Add(userInput);
processInfo.UseShellExecute = false;
```

### File upload (T1505.003)
```csharp
// ✅ Allowlist the extension, verify magic bytes, then make it unexecutable
if (!allowed.Contains(ext)) return Reject();
if (!await MatchesMagicBytesAsync(stream, ext)) return Reject();

var stored = $"{Guid.NewGuid():N}{ext}";            // you choose the name
var path = Path.Combine("/var/uploads", stored);    // outside the web root
File.SetUnixFileMode(path, UserRead | UserWrite);   // no execute bit
// Serve with: X-Content-Type-Options: nosniff + Content-Disposition: attachment

// ❌ Don't scan binary uploads for "eval(" — real PDFs match, encoded shells don't
```

### Export budget (T1213, T1567)
```python
# ✅ A fixed limit you can defend, decided BEFORE the query runs
if requested_rows > policy.max_rows_per_request:
    raise ExportDenied("request too large")
if used_this_hour + requested_rows > policy.max_rows_per_hour:
    emit("T1567", subject, used_this_hour, requested_rows)
    raise ExportDenied("hourly budget exhausted")

# ❌ Not an anomaly score — nobody can debug "0.79" at 3am
```

### Step-up from IdP signals (T1078)
```javascript
// ✅ Consume the claims the IdP already issued; don't recompute risk
if (claims.risk_level === 'high') return deny();
if (policy.requireAcr === 'mfa' && claims.acr !== 'mfa') return stepUp();
if (now - claims.auth_time > policy.maxCredentialAge) return stepUp();
// RFC 9470: WWW-Authenticate: Bearer error="insufficient_user_authentication"
```

### Tamper-evident logging (T1070)
```csharp
// ✅ Hash chain makes local edits detectable
entry.PreviousHash = lastHash;
entry.Hash = SHA256(entry.Data + entry.PreviousHash);

// ⚠️ Detects tampering; does not prevent it. Anchor the tip hash off-host,
//    and ship entries to a SIEM — that's what preserves the evidence.
```

### Secrets (T1552)
```csharp
// ❌ NEVER
private const string ApiKey = "sk_live_1234...";

// ✅ Configuration providers, workload identity
var client = new SecretClient(vaultUri, new DefaultAzureCredential());

// ✅ Better still: identity-based access to the resource, so there's no secret
```

## Technique coverage

| ID | Name | Tactic | Sample |
|----|------|--------|--------|
| T1059 | Command and Scripting Interpreter | Execution | `CommandInjection.cs` |
| T1070 | Indicator Removal | Defense Evasion | `TamperEvidentLogger.cs` |
| T1078 | Valid Accounts | Persistence | `ResourceAuthorization.cs` |
| T1185 | Browser Session Hijacking | Collection | `SessionSecurity.cs` |
| T1505.003 | Web Shell | Persistence | `FileUploadValidation.cs` |
| T1550.004 | Web Session Cookie | Defense Evasion | `SessionSecurity.cs` |
| T1552 | Unsecured Credentials | Credential Access | `SecretsManagement.cs` |

## Talk flow (suggested)

**1. Injection boundaries (5 min)** — vulnerable ping endpoint, live
`"google.com && whoami"`, then `ArgumentList`.
Takeaway: **never let input become a program.**

**2. Authorization (5 min)** — valid token, someone else's record.
Takeaway: **authenticated is not authorized, and no IdP can fix this for you.**

**3. Credential access (5 min)** — hardcoded secrets, git history, Key Vault.
Takeaway: **configuration, not code — and rotate before you delete.**

**4. Uploads and persistence (5 min)** — why content scanning fails, then
non-executable storage.
Takeaway: **if it can't execute, the contents stop mattering.**

**5. Exfiltration (5 min)** — individually-legal requests, then the budget.
Takeaway: **bound the aggregate.**

## Demo commands

```bash
# Command injection
curl "http://localhost:5000/api/vulnerable/ping?host=google.com%20%26%26%20whoami"
curl "http://localhost:5000/api/secure/ping?host=google.com"

# Broken object-level authorization — the whole demo is changing one digit
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/vulnerable/documents/$MINE
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/vulnerable/documents/$THEIRS

# Upload a renamed web shell — magic-byte check rejects it
curl -X POST -F "file=@shell.php;filename=avatar.png" http://localhost:5000/api/uploads

# Secrets in git history
git log -p | grep -iE "password|api.?key"
```

## Questions to anticipate

**Q: Isn't this all handled by our identity provider?**
A: The credential attacks are — configure those there. Object authorization,
export limits, and input boundaries are not, and never will be, because they
depend on your data model.

**Q: Are these production-ready?**
A: No. They are educational. Extract the patterns; the in-memory state in
particular needs a distributed store.

**Q: What about other languages?**
A: The boundaries are identical. Python and JavaScript versions are in
`samples/python/` and `samples/javascript/`.

**Q: Why 404 instead of 403 on an authorization failure?**
A: A 403 confirms the record exists, which turns the status code into an
enumeration oracle.

**Q: Won't export limits break legitimate bulk work?**
A: Give that work a reviewed path — an async job, an approved role — rather than
raising the limit for everyone.
