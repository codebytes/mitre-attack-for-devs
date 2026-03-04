---
marp: true
theme: custom-default
paginate: true
footer: '@Chris_L_Ayers - https://chris-ayers.com'
---

<!-- _footer: 'https://github.com/codebytes/mitre-attack-for-devs' -->

![bg](./img/crooked-line-bg.svg)

<style scoped>
h1, h2 { color: #ffffff; text-shadow: 0 0 20px rgba(0,0,0,0.9), 0 0 40px rgba(0,0,0,0.7); }
h2 { color: #00ff88; }
</style>

# <!-- fit --> MITRE ATT&CK for Developers

## <!-- fit --> The Crooked Line: How Attackers Really Operate

<!-- Attackers don't follow a straight line. They zigzag, backtrack, pivot, and adapt. This talk explores how the MITRE ATT&CK framework maps these crooked paths — and what developers can do to straighten out their defenses. The background illustrates the contrast: the dashed line is the path defenders expect, and the red crooked line is how attacks actually unfold across tactics like reconnaissance, lateral movement, and exfiltration. -->

---

![bg left:40%](./img/portrait.png)

## Chris Ayers

### Principal Software Engineer<br>Azure CXP AzRel<br>Microsoft

<i class="fa-brands fa-bluesky"></i> BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
<i class="fa-brands fa-linkedin"></i> LinkedIn: - [chris\-l\-ayers](https://linkedin.com/in/chris-l-ayers/)
<i class="fa fa-window-maximize"></i> Blog: [https://chris-ayers\.com/](https://chris-ayers.com/)
<i class="fa-brands fa-github"></i> GitHub: [Codebytes](https://github.com/codebytes)
<i class="fa-brands fa-mastodon"></i> Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)
~~<i class="fa-brands fa-twitter"></i> Twitter: @Chris_L_Ayers~~

<!-- Quick intro — I'm Chris, a Senior Software Engineer at Microsoft. I spend a lot of time thinking about how developers can build more secure applications without needing a PhD in cybersecurity. -->

---

## Agenda

- The Security Challenge for Developers
- Understanding OWASP vs MITRE ATT&CK
- ATT&CK Framework Deep Dive
- 7 Critical Technique Categories
- Practical Implementation Strategies
- Building ATT&CK-Aware Applications

<!-- Here's our roadmap. We'll start with the problem, compare two major frameworks, then dive deep into real attack techniques with code examples. By the end, you'll have practical patterns you can use tomorrow. -->

---

## The Security Challenge

- **Growing attack surface**: APIs, microservices, cloud infrastructure
- **Sophisticated adversaries**: Nation-states, organized crime, insider threats
- **Complex attack chains**: Multiple techniques chained together
- **Traditional defenses**: Often focus on single points of failure
- **Reality**: Attackers adapt faster than our defenses

<!-- The attack surface has exploded. We're not just building monoliths anymore — we have APIs, microservices, serverless, and cloud infrastructure. And attackers don't just try one thing. They chain techniques together in complex kill chains. Our defenses need to evolve beyond "patch and pray." -->

---

## What is OWASP?

- **Open Web Application Security Project** - community-driven security standards
- **OWASP Top 10 2025**: Broken Access Control, Cryptographic Failures, Injection, etc.
- **Strengths**: Vulnerability classification, remediation guidance, prevention focus
- **Approach**: "Here's what can break in your application"

<!-- Most developers know OWASP. It's fantastic for understanding vulnerabilities — what can go wrong in your code. But it's fundamentally a prevention-focused, vulnerability-centric view. It answers "what's broken" but doesn't tell you much about who's attacking or how they actually behave. -->

---

## What is MITRE ATT&CK?

- **Origin**: MITRE Corporation, 2013, FMX (Fort Meade Experiment)
- **Purpose**: Knowledge base of adversary tactics, techniques, and procedures (TTPs)
- **Enterprise Matrix**: 14 tactics, 200+ techniques, 400+ sub-techniques
- **Real-world basis**: Derived from actual cyber attacks and threat intelligence
- **Approach**: "Here's how attackers actually operate"

<!-- MITRE ATT&CK flips the perspective. Instead of cataloging vulnerabilities, it catalogs attacker behavior. It started at Fort Meade when MITRE researchers studied real adversaries on a network. With over 200 techniques mapped from real-world attacks, it's the most comprehensive map of how hackers actually operate. -->

---

## MITRE Cybersecurity Ecosystem

![center](./img/mitre-ecosystem.drawio.png)

<!-- ATT&CK isn't the only framework from MITRE. D3FEND maps defensive countermeasures, ATLAS covers AI/ML threats, and ENGAGE provides adversary engagement strategies. Together they form a comprehensive ecosystem. But ATT&CK is the foundation — and the most relevant for developers. -->

---

## ATT&CK Structure

- **Tactics**: The "why" of an attack (e.g., Initial Access, Persistence)
- **Techniques**: The "how" of an attack (e.g., Spear Phishing, Valid Accounts)
- **Sub-techniques**: Specific implementations (e.g., Spear Phishing via Email)
- **Procedures**: Real-world examples of technique usage by threat actors

<!-- Think of it as a hierarchy. Tactics are the goals — "I want to get initial access." Techniques are how — "I'll use spear phishing." Sub-techniques get specific — "I'll send a phishing email with a malicious attachment." And procedures are documented cases where real threat groups actually did this. -->

---

## The 14 ATT&CK Tactics

![center](./img/14-attack-tactics.drawio.png)

<!-- This is the kill chain — the crooked line from our title slide. Notice how it's grouped: Pre-Attack for reconnaissance, Get In for initial compromise, Stay In for maintaining access, and Act for achieving objectives. Attackers don't always go linearly — they loop back, skip steps, and adapt. -->

---

## OWASP vs ATT&CK

<div class="columns">
<div>

### OWASP
- **Focus**: Vulnerabilities
- **Perspective**: "What breaks"
- **Approach**: Prevention-first
- **Scope**: Application layer

</div>
<div>

### MITRE ATT&CK
- **Focus**: Adversary behavior
- **Perspective**: "What attackers do"
- **Approach**: Detection-oriented
- **Scope**: Full attack lifecycle

</div>
</div>

<!-- Side by side, you can see the difference. OWASP says "your SQL query is injectable." ATT&CK says "an attacker will exploit your public-facing application, escalate privileges, move laterally, and exfiltrate data." Both views are essential — one prevents the hole, the other detects the intruder. -->

---

## Why Both?

> "OWASP prevents vulnerabilities. ATT&CK detects adversary behavior."

- **Complementary approaches**: Prevention + Detection
- **Real-world attacks**: Use vulnerability chains, not single exploits
- **Defense in depth**: Multiple security perspectives
- **Complete coverage**: Technical vulnerabilities + adversary techniques

<!-- The key insight: real-world breaches are never a single vulnerability. They're chains of techniques. SolarWinds was supply chain compromise leading to lateral movement leading to data exfiltration. You need prevention AND detection to handle the full lifecycle. -->

---

## Mapping OWASP to ATT&CK

| OWASP Category | ATT&CK Techniques |
|----------------|------------------|
| Broken Access Control | T1078 (Valid Accounts), T1098 (Account Manipulation) |
| Injection | T1190 (Exploit Public-Facing App), T1059 (Command Injection) |
| Security Misconfiguration | T1552 (Unsecured Credentials), T1212 (Exploitation for Credential Access) |
| Cryptographic Failures | T1555 (Credentials from Password Stores) |
| Server-Side Request Forgery | T1090 (Proxy), T1572 (Protocol Tunneling) |

<!-- This mapping is incredibly useful. When you fix an OWASP vulnerability, you're actually blocking specific ATT&CK techniques. Fixing SQL injection doesn't just close a bug — it blocks T1190, which is the front door for dozens of attack chains. Understanding this connection helps you prioritize what to fix first. -->

---

# <!-- fit --> Let's Think Like Attackers

<!-- Now we shift gears. For the next section, I want you to put on a black hoodie — metaphorically. We're going to look at real code through the eyes of an attacker and then see how to defend it. -->

---

## The Kill Chain: Expectation vs Reality

![center w:1050 h:500](./img/expect-vs-reality.svg)

<!-- This is the core insight of the talk. Defenders build straight-line defenses — firewall, IDS, patch management. But attackers zigzag, loop back, escalate, discover new targets, and escalate again. ATT&CK captures this messy reality that a linear kill chain model misses. -->

---

# <!-- fit --> Initial Access & Credential Attacks

<!-- This is where every attack begins — getting that first foothold. Whether it's exploiting a web vulnerability, stealing credentials, or phishing, the attacker needs a way in. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1190 | Exploit Public-Facing Application | Web app vulnerabilities |
| T1078 | Valid Accounts | Compromised legitimate credentials |
| T1110 | Brute Force | Password spraying, credential stuffing |
| T1566 | Phishing | Social engineering for credentials |

<!-- These are the most common initial access techniques. T1190 is your classic web app exploit — SQL injection, XSS, etc. T1078 is even scarier — the attacker has real, valid credentials. Brute force and phishing are how they get those credentials in the first place. -->

---

## Vulnerable Code: SQL Injection (T1190)

```python
# VULNERABLE - Direct string concatenation enables T1190
@app.route('/users')
def get_user():
    user_id = request.args.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # T1190: SQL Injection vulnerability
    return cursor.fetchall()

# Attack: /users?id=1 OR 1=1--
```

<!-- Classic SQL injection. The attacker passes "1 OR 1=1--" as the ID, which dumps the entire users table. This is the number one way attackers exploit public-facing applications. Simple string concatenation is all it takes to open the door. -->

---

## Defended Code: Parameterized Queries

```python
# DEFENDED - Parameterized queries prevent T1190
@app.route('/users')
def get_user():
    user_id = request.args.get('id')
    if not user_id.isdigit():
        return "Invalid input", 400
    # T1190 Prevention: Parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    if not result:
        return "User not found", 404  # T1087 Prevention: Consistent responses
    return result[0]
```

<!-- The fix is straightforward — parameterized queries. But notice we also added input validation and consistent error responses. The consistent 404 prevents T1087 account discovery — attackers can't tell which user IDs exist based on different error messages. Defense in depth. -->

---

## Credential Stuffing Detection (T1110.004)

```javascript
// T1110.004 Detection: Credential stuffing patterns
class CredentialStuffingDetector {
    detectSuspiciousLogin(loginData) {
        const { username, ip, userAgent, timestamp } = loginData;
        // Multiple accounts from same IP
        if (this.countAccountsFromIP(ip) > 10) {
            this.logTechnique("T1110.004", { ip, type: "multiple_accounts" });
            return true;
        }
        // Rapid login attempts across accounts  
        if (this.getRateFromIP(ip) > 100) {
            this.logTechnique("T1110.004", { ip, type: "high_velocity" });
            return true;
        }
        return false;
    }
}
```

<!-- Credential stuffing uses breached password databases to try known username/password pairs at scale. Detection is key here — look for many accounts being tried from the same IP, or unusually rapid login attempts. This is behavioral detection, not vulnerability prevention. -->

---

# <!-- fit --> Execution & Code Injection

<!-- Once attackers get in, they need to execute code. This section covers how they run malicious commands through your application. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1059 | Command & Scripting Interpreter | OS command injection |
| T1203 | Exploitation for Client Execution | Client-side code execution |
| T1055 | Process Injection | Injecting into legitimate processes |

<!-- Command injection is when user input ends up in an OS command. Exploitation for client execution targets the user's browser or client application. Process injection is more advanced — injecting code into running processes. As developers, we mostly encounter T1059. -->

---

## Vulnerable Code: Command Injection (T1059)

```csharp
// VULNERABLE - Direct command execution enables T1059
[HttpPost]
public IActionResult ProcessFile(string filename)
{
    // T1059: Command injection vulnerability
    var command = $"convert {filename} output.pdf";
    var process = Process.Start("cmd.exe", $"/c {command}");
    process.WaitForExit();
    
    return Ok("File processed");
}

// Attack payload: file.jpg; rm -rf / --
```

<!-- This is terrifying. The filename goes directly into a shell command. An attacker sends "file.jpg; rm -rf /" and suddenly your server is wiping itself. Or worse — they install a reverse shell and maintain persistent access. Never concatenate user input into shell commands. -->

---

## Defended Code: Command Allowlisting

```csharp
// DEFENDED - Strict input validation and allowlisting
[HttpPost]
public IActionResult ProcessFile(string filename)
{
    if (!IsValidFilename(filename))
        return BadRequest("Invalid filename");
    // T1059 Prevention: No shell, direct process call
    var processInfo = new ProcessStartInfo
    {
        FileName = "imagemagick.exe",
        Arguments = string.Join(" ", new[] { filename, "output.pdf" }.Select(EscapeArg)),
        UseShellExecute = false
    };
    using var process = Process.Start(processInfo);
    process?.WaitForExit();
    return Ok("File processed safely");
}
```

<!-- The defended version never uses a shell. We validate the filename, use an allowlist of commands, escape arguments, and call the binary directly with ProcessStartInfo. No shell means no shell injection. Always avoid UseShellExecute when processing user input. -->

---

## Unsafe Deserialization (T1203)

```python
# VULNERABLE - Unsafe deserialization enables T1203
import pickle
@app.route('/api/data', methods=['POST'])
def process_data():
    obj = pickle.loads(request.data)  # Code execution risk!
    return process_object(obj)

# DEFENDED - Safe deserialization with JSON
import json
@app.route('/api/data', methods=['POST'])  
def process_data():
    try:
        data = json.loads(request.data)  # T1203 Prevention
        if not validate_schema(data):
            return "Invalid data format", 400
        return process_object(data)
    except json.JSONDecodeError:
        return "Invalid JSON", 400
```

<!-- Pickle deserialization is essentially arbitrary code execution disguised as data parsing. The fix is simple — use JSON instead. If you must deserialize complex objects, use schema validation. Never deserialize untrusted data with pickle, YAML's unsafe loader, or Java's ObjectInputStream. -->

---

# <!-- fit --> Persistence & Session Hijacking

<!-- Attackers don't want to re-exploit every time. Once they're in, they want to stay in. This is where persistence techniques come in — and session hijacking is one of the most common web-specific methods. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1098 | Account Manipulation | Modifying user accounts for persistence |
| T1185 | Browser Session Hijacking | Stealing and reusing session tokens |
| T1505.003 | Web Shell | Server-side persistence mechanisms |

<!-- Account manipulation means creating backdoor accounts or elevating privileges on existing ones. Session hijacking steals active sessions — why crack passwords when you can steal the cookie? Web shells are the scariest — a persistent backdoor file on your server that gives the attacker a command line. -->

---

## Vulnerable Session Management

```javascript
// VULNERABLE - Weak session security enables T1185
app.use(session({
    secret: 'hardcoded-secret',       // T1552: Hardcoded secret
    resave: false, saveUninitialized: false,
    cookie: {
        secure: false,                // T1185: No HTTPS requirement
        httpOnly: false,              // T1185: XSS vulnerable
        maxAge: 24 * 60 * 60 * 1000  // T1185: Long expiration
    }
}));
// No session validation or rotation
app.get('/api/data', (req, res) => {
    if (req.session.user) return res.json(getData(req.session.user));
    res.status(401).send('Unauthorized');
});
```

<!-- Count the vulnerabilities: hardcoded secret means anyone with source access can forge sessions, no HTTPS means cookies fly in plaintext, no httpOnly means JavaScript can steal them via XSS, and 24-hour expiration gives attackers a huge window. Plus, no session validation or rotation means a stolen session works forever. -->

---

## Defended Session Management

```javascript
// DEFENDED - Secure session handling prevents T1185
app.use(session({
    secret: process.env.SESSION_SECRET,   // T1552 Prevention
    resave: false, saveUninitialized: false,
    rolling: true,                        // Session rotation
    cookie: {
        secure: true, httpOnly: true,     // HTTPS + XSS protection
        maxAge: 15 * 60 * 1000,           // Short expiration
        sameSite: 'strict'                // CSRF protection
    }
}));
// T1185 Prevention: Session fingerprinting
function validateSession(req, res, next) {
    if (!req.session.user) return res.status(401).send('Unauthorized');
    const fingerprint = generateFingerprint(req);
    if (req.session.fingerprint !== fingerprint) {
        req.session.destroy();
        return res.status(401).send('Session security violation');
    }
    next();
}
```

<!-- The defended version addresses every issue: environment-based secrets, HTTPS-only cookies, httpOnly flag, short 15-minute expiry with rolling refresh, SameSite protection, and session fingerprinting. The fingerprint ties the session to the client's characteristics — if someone steals the cookie but has a different fingerprint, we kill the session. -->

---

## Web Shell Detection (T1505.003)

```csharp
// T1505.003 Detection: Web shell upload monitoring
public class FileUploadValidator {
    private readonly string[] _suspiciousPatterns = {
        "eval(", "exec(", "system(", "<?php", "<%", "<script", "cmd.exe"
    };
    public bool ValidateUpload(IFormFile file) {
        var allowed = new[] { ".jpg", ".png", ".pdf", ".docx" };
        var ext = Path.GetExtension(file.FileName).ToLower();
        if (!allowed.Contains(ext)) {
            LogSecurityEvent("T1505.003", $"Bad extension: {ext}");
            return false;
        }
        using var reader = new StreamReader(file.OpenReadStream());
        var content = reader.ReadToEnd();
        foreach (var p in _suspiciousPatterns)
            if (content.Contains(p, StringComparison.OrdinalIgnoreCase)) {
                LogSecurityEvent("T1505.003", $"Web shell: {p}");
                return false;
            }
        return true;
    }
}
```

<!-- Web shells are how attackers maintain persistent access to your server. This validator checks both file extensions and content patterns. A file named "profile.jpg" that contains "<?php eval(" is clearly a web shell. Always validate upload content, not just the extension — attackers can double-extend filenames or use polyglot files. -->

---

# <!-- fit --> Credential Access & Secrets

<!-- Credentials are the keys to the kingdom. Attackers know that developers often leave secrets lying around in code, config files, and environment variables. Let's look at the wrong way and the right way. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1552 | Unsecured Credentials | Hardcoded secrets, config files |
| T1555 | Credentials from Password Stores | Browser/app credential extraction |
| T1528 | Steal Application Access Token | API tokens, OAuth tokens |

<!-- T1552 is huge — hardcoded credentials in source code are found in almost every codebase audit. T1555 targets credential stores like browser password managers. T1528 is about stealing OAuth tokens and API keys from running applications. All three are preventable with proper secrets management. -->

---

## Bad Secrets Management - All Languages

```python
# PYTHON - BAD: T1552 vulnerability
DATABASE_URL = "postgres://user:password123@localhost/mydb"  # Hardcoded
API_KEY = "sk-1234567890abcdef"  # In source code
```

```csharp
// C# - BAD: T1552 vulnerability  
public class Config
{
    public static string ConnectionString = "Server=.;Database=MyApp;User Id=sa;Password=MyPassword123;";  // Hardcoded
    public static string ApiKey = "Bearer abc123def456";  // In source code
}
```

```javascript
// JAVASCRIPT - BAD: T1552 vulnerability
const config = {
    dbPassword: 'mypassword123',  // Hardcoded
    jwtSecret: 'supersecretkey',  // In source code
    apiKey: 'pk_live_1234567890'  // Version controlled
};
```

<!-- I see this in code reviews all the time. Passwords in connection strings, API keys in config objects, secrets committed to git. Once a secret hits version control, it's there forever — even if you delete it, it's in the git history. Tools like truffleHog and GitLeaks specifically scan for these patterns. -->

---

## Good Secrets Management - Python & C\#

```python
# PYTHON: T1552 prevention — Managed Identity + Key Vault
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# No API keys! Managed Identity authenticates automatically
credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net", credential=credential)
db_conn = client.get_secret("db-connection-string").value
```

```csharp
// C#: T1552 prevention — Managed Identity + RBAC + Key Vault
var credential = new DefaultAzureCredential(); // No secrets needed
var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net"), credential);
// RBAC: App's managed identity has Key Vault Secrets User role
var connStr = (await client.GetSecretAsync("db-connection")).Value.Value;
```

<!-- The right approach: use Managed Identity — your app authenticates to Azure without any credentials in code. RBAC controls who can access what in Key Vault. No API keys, no secrets in config, no rotation headaches. DefaultAzureCredential works locally with your dev credentials and in production with managed identity. -->

---

## Good Secrets Management - JavaScript

```javascript
// JAVASCRIPT: T1552 prevention — Managed Identity + Key Vault
const { SecretClient } = require("@azure/keyvault-secrets");
const { DefaultAzureCredential } = require("@azure/identity");

// No API keys! Managed Identity handles auth via RBAC
const credential = new DefaultAzureCredential();
const client = new SecretClient(
    "https://myvault.vault.azure.net", credential);

async function getDbConnection() {
    const secret = await client.getSecret("db-connection-string");
    return secret.value;  // Fetched at runtime, never in code
}
```

<!-- Same pattern in JavaScript with Azure Key Vault and Managed Identity. The key principle across all languages: no secrets in code, no API keys, authenticate with identity not credentials. Works with Azure, AWS IAM Roles, and GCP Workload Identity too. -->

---

## Secrets Scanner Implementation

```python
# T1552 Prevention: Automated secrets detection
import re

class SecretsScanner:
    patterns = [
        (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded Password'),
        (r'api[_-]?key\s*[=:]\s*["\'][^"\']{16,}["\']', 'API Key'),
        (r'sk-[a-zA-Z0-9]{32,}', 'Secret Key'),
        (r'-----BEGIN [A-Z ]+-----', 'Private Key')
    ]
    def scan_file(self, filepath):
        violations = []
        with open(filepath, 'r') as f:
            content = f.read()
            for pattern, desc in self.patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    violations.append({
                        'file': filepath,
                        'line': content[:match.start()].count('\n') + 1,
                        'type': desc, 'technique': 'T1552'
                    })
        return violations
```

<!-- Automate your secret scanning! Run this in CI/CD pipelines and as pre-commit hooks. It catches common patterns like hardcoded passwords, API keys, and private keys before they ever reach version control. Tools like GitHub Advanced Security, GitLeaks, and truffleHog do this at enterprise scale. -->

---

# <!-- fit --> Defense Evasion & Log Tampering

<!-- This is the sneaky stuff. Once attackers are in, they don't want to be detected. They'll tamper with logs, obfuscate their tools, and masquerade as legitimate processes. If your logging can be manipulated, your incident response is blind. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1027 | Obfuscated Files/Information | Hiding malicious content |
| T1070 | Indicator Removal on Host | Log deletion/tampering |
| T1036 | Masquerading | Appearing legitimate |

<!-- T1027 is about hiding malicious payloads — encoding, encryption, packing. T1070 is log tampering — deleting or modifying logs to cover tracks. T1036 is masquerading — making malicious files look like legitimate system files. These techniques make forensic investigation extremely difficult. -->

---

## Log Injection Attack (T1070)

```python
# VULNERABLE - Log injection enables T1070
import logging
logger = logging.getLogger(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not authenticate(username, password):
        logger.warning(f"Failed login for user: {username}")  # T1070!
        return "Invalid credentials", 401
    return "Login successful"
# Attack: "admin\n[INFO] Successful login for admin"
# Creates fake success log entry
```

<!-- Log injection is subtle and devastating. The attacker's username contains a newline and a fake log entry. Your log file now shows a successful admin login that never happened — and the real failed attempt is buried. During incident response, investigators will see "Successful login for admin" and miss the attack entirely. -->

---

## Tamper-Evident Logging (T1070 Prevention)

```csharp
// T1070 Prevention: Tamper-evident logging with hash chains
public class SecureLogger
{
    private string _lastHash = "genesis";
    public void LogSecurityEvent(string technique, string details)
    {
        var logEntry = new SecurityLogEntry {
            Timestamp = DateTime.UtcNow,
            Technique = technique,
            Details = SanitizeInput(details),      // Sanitize input
            PreviousHash = _lastHash
        };
        // Cryptographic hash chain
        logEntry.Hash = ComputeHash(
            $"{logEntry.Timestamp}{logEntry.Technique}{logEntry.Details}{_lastHash}");
        _lastHash = logEntry.Hash;
        WriteToImmutableStore(logEntry);            // Immutable storage
        await SendToSIEM(logEntry);                 // External SIEM
    }
    private string SanitizeInput(string input) =>
        Regex.Replace(input ?? "", @"[\r\n\t\f]", "_");
}
```

<!-- The solution is tamper-evident logging. We sanitize input to remove newlines, use cryptographic hash chains so any modification is detectable, write to immutable storage like Azure Append Blobs or AWS CloudTrail, and send copies to an external SIEM. If an attacker modifies one log entry, the hash chain breaks and we know immediately. -->

---

## Immutable Logging Architecture

![center](./img/immutable-logging.drawio.png)

<!-- This architecture ensures that even if an attacker gets root access, they can't silently erase their tracks. The local buffer, encrypted storage, and external SIEM create multiple independent records. Tamper detection compares them — if they disagree, someone modified the logs. -->

---

# <!-- fit --> Supply Chain Compromise

<!-- This is the technique that keeps security teams up at night. Why attack your code when they can attack the code you depend on? SolarWinds, Log4Shell, and the event-stream incident all showed how devastating supply chain attacks can be. -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1195 | Supply Chain Compromise | Compromising upstream dependencies |
| T1195.001 | Compromise Software Dependencies | Malicious packages |

<!-- T1195 is the broad category — any compromise of something upstream of you. T1195.001 specifically targets software dependencies — the npm packages, PyPI packages, and NuGet packages we all depend on. The average application has hundreds of dependencies, each one a potential attack vector. -->

---

## Supply Chain Attack Examples

- **NPM**: `event-stream` package (2018) - 8M downloads, Bitcoin wallet stealer
- **PyPI**: Typosquatting attacks - `urllib3` vs `urllib4`  
- **NuGet**: Dependency confusion - internal vs public packages
- **Docker**: Compromised base images with embedded malware

<!-- The event-stream incident is a masterclass in supply chain attacks. A maintainer handed off a popular package to a new contributor who added a Bitcoin-stealing payload. 8 million weekly downloads. Typosquatting creates packages with similar names hoping for typos. Dependency confusion exploits the gap between public and private registries. -->

---

## Dependency Verification - All Ecosystems

```bash
# NPM - T1195.001 Prevention
npm audit --audit-level high
npm ci --only=production  # Use lockfile exactly
npm install --package-lock-only  # Generate lockfile without install

# Python - T1195.001 Prevention  
pip install --require-hashes -r requirements.txt
pip-audit  # Vulnerability scanning
bandit -r .  # Security static analysis

# .NET - T1195.001 Prevention
dotnet list package --vulnerable --include-transitive
dotnet nuget verify MyPackage.1.0.0.nupkg  # Package signature verification
```

<!-- Every ecosystem has tools for this. npm audit, pip-audit, and dotnet list --vulnerable are your first line of defense. Use lockfiles religiously — npm ci uses the exact lockfile, and pip's --require-hashes verifies every package against known checksums. Run these in CI/CD to catch issues before deployment. -->

---

## Package Integrity Validation

```python
# T1195.001 Prevention: Package integrity validation
import hashlib, json

class PackageValidator:
    def __init__(self, lockfile_path):
        with open(lockfile_path) as f:
            self.lockfile = json.load(f)
    def validate_package(self, package_name, package_file):
        expected = self.lockfile['packages'][package_name]['integrity']
        actual = self.compute_hash(package_file)
        if actual != expected:
            self.log_security_event('T1195.001', {
                'package': package_name,
                'expected': expected, 'actual': actual,
                'alert': 'Package integrity violation detected'
            })
            return False
        return True
    def compute_hash(self, package_file):
        hasher = hashlib.sha512()
        with open(package_file, 'rb') as f:
            hasher.update(f.read())
        return f"sha512-{hasher.hexdigest()}"
```

<!-- This validator goes further — it computes the SHA-512 hash of every downloaded package and compares it against the lockfile's recorded hash. If someone tampers with a package on the registry, the hash won't match and the install is blocked. This is exactly how --require-hashes works under the hood. -->

---

## Supply Chain Security Flow

![center](./img/attack-chain-supply.drawio.png)

<!-- This is your supply chain security pipeline. Every dependency goes through integrity checks and vulnerability scanning before it's installed. Even after installation, monitoring continues — because vulnerabilities can be discovered in packages you already use. Automation is key — make this a gate in your CI/CD pipeline. -->

---

# <!-- fit --> Collection & Exfiltration

<!-- This is the endgame for many attacks. The attacker has gotten in, escalated privileges, and moved laterally. Now they want the data. How do they collect it, and how do they get it out without being noticed? -->

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1213 | Data from Information Repositories | Bulk data access |
| T1567 | Exfiltration Over Web Service | Cloud storage uploads |
| T1020 | Automated Exfiltration | Scripted data theft |

<!-- T1213 is bulk data harvesting — think SELECT * FROM customers. T1567 uses legitimate cloud services like Dropbox or Google Drive to exfiltrate data, making it hard to distinguish from normal traffic. T1020 automates the process with scripts that systematically extract and transfer data. -->

---

## Data Access Anomaly Detection

```python
# T1213 Detection: Unusual data access patterns
class DataAccessMonitor:
    def __init__(self):
        self.user_baselines = {}
    def check_access_pattern(self, user_id, query, context):
        baseline = self.get_user_baseline(user_id)
        current = {
            'records_accessed': query.estimated_rows,
            'tables_accessed': len(query.tables),
            'data_sensitivity': self.classify_sensitivity(query.tables)
        }
        score = self.calculate_anomaly_score(baseline, current)
        if score > 0.8:
            self.log_technique('T1213', {
                'user': user_id, 'score': score, 'query': query.sanitized_sql
            })
            return self.require_step_up_auth(user_id)
        return True
    def calculate_anomaly_score(self, baseline, current):
        scores = [min(abs((current[m] - baseline[m]['mean']) /
                  baseline[m]['std']) / 3.0, 1.0)
                  for m in ['records_accessed', 'tables_accessed']]
        return max(scores)
```

<!-- This is behavioral analytics in action. We baseline each user's normal data access patterns — how many records they typically access, which tables, what time of day. When someone suddenly accesses 10x their normal volume or touches sensitive tables they've never queried before, the anomaly score spikes and we trigger step-up authentication. -->

---

## API Rate Limiting with Exfil Detection

```javascript
// T1567/T1020 Prevention: Exfiltration-aware rate limiting
class ExfiltrationDetector {
    constructor() { this.tracking = new Map(); }
    async checkDataTransfer(userId, requestSize, responseSize) {
        const now = Date.now();
        const windowMs = 60 * 60 * 1000; // 1 hour
        if (!this.tracking.has(userId)) this.tracking.set(userId, []);
        const transfers = this.tracking.get(userId)
            .filter(t => now - t.timestamp < windowMs);
        transfers.push({ timestamp: now, responseSize });
        this.tracking.set(userId, transfers);
        // Bulk transfer analysis
        const total = transfers.reduce((sum, t) => sum + t.responseSize, 0);
        if (total > 100 * 1024 * 1024) { // 100MB in 1 hour
            await this.logSecurityEvent('T1567', {
                userId, totalTransferred: total,
                requestCount: transfers.length, timeWindow: '1h'
            });
            return false; // Block
        }
        return true;
    }
}
```

<!-- Traditional rate limiting counts requests. Exfiltration-aware rate limiting counts bytes. An attacker might make only 10 API calls, but if each returns 10MB of data, that's 100MB of exfiltration in minutes. By tracking cumulative transfer volume per user per time window, we can detect and block bulk data theft even at low request rates. -->

---

## Data Flow Monitoring

![center h:480](./img/data-flow-monitoring.drawio.png)

<!-- Multiple checkpoints in the data flow. Authorization happens first, then anomaly detection checks the pattern, then bulk transfer detection checks the volume, and finally rate limiting checks the frequency. Any checkpoint can block the request and alert the security team. Layered defense for data protection. -->

---

# DEMOS

<!-- Let's see some of these concepts in action with live demos. -->

---

# <!-- fit --> Practical Implementation

<!-- Now let's talk about how to actually bring all of this into your development workflow. Theory is great, but what do you do on Monday morning? -->

---

## ATT&CK-Informed Threat Modeling

![center h:480](./img/threat-modeling-loop.drawio.png)

<!-- This is your threat modeling loop. For every feature, ask: what ATT&CK techniques could target this? Then design detections, implement them, and test. The loop is continuous — as new techniques are added to ATT&CK, revisit your features. This is a shift from reactive patching to proactive defense design. -->

---

## Map Features to Techniques

| Application Feature | ATT&CK Techniques | Risk Level |
|---------------------|------------------|------------|
| User Login | T1078, T1110, T1566 | High |
| Password Reset | T1566, T1078 | High |
| Session Management | T1185, T1098 | High |
| File Upload | T1505.003, T1190 | High |
| API Endpoints | T1087, T1046, T1213 | Medium |
| Data Export | T1567, T1020, T1030 | High |
| Logging System | T1070, T1027 | Medium |
| Dependencies | T1195, T1195.001 | Medium |

<!-- This table is a cheat sheet. For every feature in your application, you can look up which ATT&CK techniques are relevant. User login maps to credential attacks. File upload maps to web shells. Data export maps to exfiltration. Use this as a starting point for your threat model — customize it for your specific application. -->

---

## Building Detection Into Code

### Key Patterns:

- **Behavioral Analytics**: Monitor user patterns vs baselines
- **Technique Logging**: Tag events with ATT&CK IDs for correlation
- **Adaptive Controls**: Risk-based authentication and authorization  
- **Honey Tokens**: Fake data/accounts to detect unauthorized access
- **Immutable Auditing**: Tamper-evident logging and monitoring

<!-- These are the five patterns we've seen throughout this talk. Behavioral analytics baseline normal behavior and flag anomalies. Technique logging uses ATT&CK IDs so your SIEM can correlate across systems. Adaptive controls increase security requirements when risk increases. Honey tokens are traps for attackers. Immutable auditing ensures your investigation data can't be tampered with. -->

---

## Defense in Depth Architecture

![center](./img/defense-in-depth.drawio.png)

<!-- Defense in depth means every layer has its own security controls. Input validation stops injection, authentication verifies identity, authorization controls access, behavioral analytics detects anomalies, threat intelligence provides context, and automated blocking responds in real-time. An attacker has to bypass ALL of these layers. -->

---

## OWASP + ATT&CK Integration

![center](./img/owasp-attack-integration.drawio.png)

<!-- This is how OWASP and ATT&CK work together in practice. OWASP gives you secure coding practices, vulnerability testing, and security reviews. ATT&CK adds behavioral monitoring, technique correlation, and threat hunting. Together, you get: Secure by Design, Monitor by Behavior, and Respond by Intelligence. -->

---

## Integration Points

| Tool/Practice | OWASP Integration | ATT&CK Integration |
|---------------|------------------|-------------------|
| SAST/DAST | Vulnerability scanning | Code pattern analysis for technique enablers |
| SIEM/Logging | Security event logging | ATT&CK technique ID correlation |
| Threat Modeling | Risk assessment | Adversary technique mapping |
| Code Review | Vulnerability checklist | Technique resistance validation |
| Penetration Testing | Vulnerability exploitation | Technique simulation |
| Incident Response | Vulnerability remediation | ATT&CK-based investigation |

<!-- For every tool and practice you already use, there's both an OWASP and ATT&CK angle. Your SAST scanner finds vulnerabilities (OWASP) and also identifies code patterns that enable specific techniques (ATT&CK). Your penetration tests can exploit vulnerabilities AND simulate real adversary technique chains. Leverage what you already have. -->

---

## Implementation Roadmap

<div class="columns3">
<div>

### Phase 1: Foundation
- Map features to ATT&CK techniques
- Secure logging with technique IDs
- Basic behavioral analytics

</div>
<div>

### Phase 2: Detection
- Anomaly detection for high-risk techniques
- Automated response workflows
- SIEM integration

</div>
<div>

### Phase 3: Advanced
- Honey tokens and deception
- Threat intelligence correlation
- Security dashboards

</div>
</div>

<!-- Don't try to boil the ocean. Phase 1 is mapping and logging — understand what you're defending and make sure you can see what's happening. Phase 2 adds active detection and automated response. Phase 3 adds advanced capabilities like deception and threat intelligence. Each phase builds on the last. -->

---

## Team Adoption Strategies

- **Training**: ATT&CK workshops for development teams
- **Process**: Include technique IDs in security requirements  
- **Tools**: Use ATT&CK Navigator for coverage visualization
- **Culture**: "Red team thinking" in design reviews
- **Metrics**: Track technique coverage and detection rates
- **Collaboration**: Regular sync between dev and security teams

<!-- Security culture is as important as security code. Train your team on ATT&CK, include technique IDs in your Jira tickets, use the ATT&CK Navigator for visual coverage maps, and encourage "red team thinking" in design reviews. Ask: "If I were an attacker, how would I abuse this feature?" -->

---

## ATT&CK Navigator

- **Tool**: [mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)
- **Purpose**: Visualize technique coverage and gaps
- **Use Cases**: 
  - Map application defenses to techniques
  - Track security control effectiveness
  - Plan security improvements
  - Communicate risk to stakeholders

<!-- The ATT&CK Navigator is a free, interactive tool for visualizing your coverage. Color-code techniques green for defended, yellow for partially covered, and red for gaps. It's incredibly powerful for communicating with stakeholders — a visual heat map of your security posture is worth a thousand bullet points. -->

---

## Start Small - Pick Your Top 3

### Recommendation for most applications:
1. **T1078 (Valid Accounts)** - Authentication monitoring
2. **T1185 (Session Hijacking)** - Session security  
3. **T1213 (Data Collection)** - Data access anomalies

### Why these first:
- **High impact** on most attack chains
- **Relatively easy** to implement
- **Immediate value** for detection
- **Foundation** for expanding coverage

<!-- Don't be overwhelmed by 200+ techniques. Start with these three: authentication monitoring catches credential abuse, session security prevents hijacking, and data access anomalies catch collection and exfiltration. These three techniques appear in almost every major breach. Master these, then expand. -->

---

# <!-- fit --> Key Takeaways

<!-- Let's wrap up with the key messages I want you to take away from this talk. -->

---

## Key Takeaways

- ✅ **OWASP + ATT&CK = Complete Security** - Prevention + Detection
- ✅ **Think Like an Attacker** - Understand adversary behavior patterns  
- ✅ **Build Detection Into Code** - Monitoring isn't just ops responsibility
- ✅ **Log ATT&CK Technique IDs** - Enable security team correlation
- ✅ **Use Behavioral Analytics** - Go beyond simple rule-based detection
- ✅ **Start Small, Iterate** - Pick 3 techniques and expand coverage

<!-- If you remember nothing else: OWASP and ATT&CK are complementary, not competing. Think like an attacker to build better defenses. Detection is a developer responsibility, not just ops. Tag your security events with ATT&CK IDs. Use behavioral analytics. And start with three techniques — don't try to cover everything at once. -->

---

<div class="columns">
<div>

## Links

- **[MITRE ATT&CK Framework](https://attack.mitre.org/)** - Main knowledge base
- **[ATT&CK Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/)** - Technique matrix
- **[ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)** - Coverage visualization
- **[OWASP Developer Guide](https://owasp.org/www-project-developer-guide/)** - Secure development
- **[D3FEND](https://d3fend.mitre.org/)** - Defensive countermeasures

</div>
<div>

## Chris Ayers

<i class="fa-brands fa-bluesky"></i> BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
<i class="fa-brands fa-linkedin"></i> LinkedIn: - [chris\-l\-ayers](https://linkedin.com/in/chris-l-ayers/)
<i class="fa fa-window-maximize"></i> Blog: [https://chris-ayers\.com/](https://chris-ayers.com/)
<i class="fa-brands fa-github"></i> GitHub: [Codebytes](https://github.com/codebytes)
<i class="fa-brands fa-mastodon"></i> Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)
~~<i class="fa-brands fa-twitter"></i> Twitter: @Chris_L_Ayers~~

</div>
</div>

<!-- Here are resources to continue your journey. The ATT&CK framework site and Navigator are your primary tools. D3FEND is MITRE's companion project that maps defensive countermeasures to techniques. And please reach out — I love talking about this stuff. -->

---

# Questions?

![bg right](./img/owl.png)

<!-- Thank you! I'm happy to take questions. If we run out of time, catch me in the hallway or reach out on BlueSky or LinkedIn. -->