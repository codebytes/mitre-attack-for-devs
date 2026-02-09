---
marp: true
theme: custom-default
paginate: true
footer: '@Chris_L_Ayers - https://chris-ayers.com'
---

<!-- _footer: 'https://github.com/codebytes/mitre-attack-for-devs' -->

# MITRE ATT&CK for Developers

## Beyond OWASP

---

![bg left:40%](./img/portrait.png)

## Chris Ayers

### Senior Software Engineer<br>Azure CXP AzRel<br>Microsoft

<i class="fa-brands fa-bluesky"></i> BlueSky: [@chris-ayers.com](https://bsky.app/profile/chris-ayers.com)
<i class="fa-brands fa-linkedin"></i> LinkedIn: - [chris\-l\-ayers](https://linkedin.com/in/chris-l-ayers/)
<i class="fa fa-window-maximize"></i> Blog: [https://chris-ayers\.com/](https://chris-ayers.com/)
<i class="fa-brands fa-github"></i> GitHub: [Codebytes](https://github.com/codebytes)
<i class="fa-brands fa-mastodon"></i> Mastodon: [@Chrisayers@hachyderm.io](https://hachyderm.io/@Chrisayers)
~~<i class="fa-brands fa-twitter"></i> Twitter: @Chris_L_Ayers~~

---

## Agenda

- The Security Challenge for Developers
- Understanding OWASP vs MITRE ATT&CK
- ATT&CK Framework Deep Dive
- 7 Critical Technique Categories
- Practical Implementation Strategies
- Building ATT&CK-Aware Applications

---

## The Security Challenge

- **Growing attack surface**: APIs, microservices, cloud infrastructure
- **Sophisticated adversaries**: Nation-states, organized crime, insider threats
- **Complex attack chains**: Multiple techniques chained together
- **Traditional defenses**: Often focus on single points of failure
- **Reality**: Attackers adapt faster than our defenses



---

## What is OWASP?

- **Open Web Application Security Project** - community-driven security standards
- **OWASP Top 10 2025**: Broken Access Control, Cryptographic Failures, Injection, etc.
- **Strengths**: Vulnerability classification, remediation guidance, prevention focus
- **Approach**: "Here's what can break in your application"



---

## What is MITRE ATT&CK?

- **Origin**: MITRE Corporation, 2013, FMX (Fort Meade Experiment)
- **Purpose**: Knowledge base of adversary tactics, techniques, and procedures (TTPs)
- **Enterprise Matrix**: 14 tactics, 200+ techniques, 400+ sub-techniques
- **Real-world basis**: Derived from actual cyber attacks and threat intelligence
- **Approach**: "Here's how attackers actually operate"



---

## ATT&CK Structure

- **Tactics**: The "why" of an attack (e.g., Initial Access, Persistence)
- **Techniques**: The "how" of an attack (e.g., Spear Phishing, Valid Accounts)
- **Sub-techniques**: Specific implementations (e.g., Spear Phishing via Email)
- **Procedures**: Real-world examples of technique usage by threat actors



---

## The 14 ATT&CK Tactics

<div class="mermaid">
flowchart LR
    subgraph "Pre-Attack"
        A[Reconnaissance] --> B[Resource Development]
    end
    subgraph "Get In"
        C[Initial Access] --> D[Execution] --> E[Persistence] --> F[Privilege Escalation]
    end
    subgraph "Stay In"
        G[Defense Evasion] --> H[Credential Access] --> I[Discovery] --> J[Lateral Movement]
    end
    subgraph "Act"
        K[Collection] --> L[Command and Control] --> M[Exfiltration] --> N[Impact]
    end
    B --> C
    F --> G
    J --> K
</div>



---

<!-- _class: columns -->

## OWASP vs ATT&CK

<div>

### OWASP
- **Focus**: Vulnerabilities
- **Perspective**: "What breaks"
- **Approach**: Prevention-first
- **Scope**: Application layer
- **Mindset**: Defensive

</div>
<div>

### MITRE ATT&CK
- **Focus**: Adversary behavior  
- **Perspective**: "What attackers do"
- **Approach**: Detection-oriented
- **Scope**: Full attack lifecycle
- **Mindset**: Adversarial

</div>


---

## Why Both?

> "OWASP prevents vulnerabilities. ATT&CK detects adversary behavior."

- **Complementary approaches**: Prevention + Detection
- **Real-world attacks**: Use vulnerability chains, not single exploits
- **Defense in depth**: Multiple security perspectives
- **Complete coverage**: Technical vulnerabilities + adversary techniques


---

## Mapping OWASP to ATT&CK

| OWASP Category | ATT&CK Techniques |
|----------------|------------------|
| Broken Access Control | T1078 (Valid Accounts), T1098 (Account Manipulation) |
| Injection | T1190 (Exploit Public-Facing App), T1059 (Command Injection) |
| Security Misconfiguration | T1552 (Unsecured Credentials), T1212 (Exploitation for Credential Access) |
| Cryptographic Failures | T1555 (Credentials from Password Stores) |
| Server-Side Request Forgery | T1090 (Proxy), T1572 (Protocol Tunneling) |


---

# <!-- fit --> Let's Think Like Attackers

---

# <!-- fit --> Initial Access & Credential Attacks

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1190 | Exploit Public-Facing Application | Web app vulnerabilities |
| T1078 | Valid Accounts | Compromised legitimate credentials |
| T1110 | Brute Force | Password spraying, credential stuffing |
| T1566 | Phishing | Social engineering for credentials |


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


---

## Defended Code: Parameterized Queries

```python
# DEFENDED - Parameterized queries prevent T1190
@app.route('/users')
def get_user():
    user_id = request.args.get('id')
    
    # Input validation
    if not user_id.isdigit():
        return "Invalid input", 400
        
    # T1190 Prevention: Parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    # T1087 Prevention: Consistent responses
    result = cursor.fetchall()
    if not result:
        return "User not found", 404
    return result[0]
```

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


---

# <!-- fit --> Execution & Code Injection

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1059 | Command & Scripting Interpreter | OS command injection |
| T1203 | Exploitation for Client Execution | Client-side code execution |
| T1055 | Process Injection | Injecting into legitimate processes |


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


---

## Defended Code: Command Allowlisting

```csharp
// DEFENDED - Strict input validation and allowlisting
[HttpPost]
public IActionResult ProcessFile(string filename)
{
    // T1059 Prevention: Input validation
    if (!IsValidFilename(filename))
        return BadRequest("Invalid filename");
        
    // T1059 Prevention: Command allowlisting
    var allowedCommands = new[] { "convert", "resize", "compress" };
    var safeArgs = new[] { filename, "output.pdf" };
    
    var processInfo = new ProcessStartInfo
    {
        FileName = "imagemagick.exe",
        Arguments = string.Join(" ", safeArgs.Select(EscapeArg)),
        UseShellExecute = false
    };
    
    using var process = Process.Start(processInfo);
    process?.WaitForExit();
    
    return Ok("File processed safely");
}
```

---

## Unsafe Deserialization (T1203)

```python
# VULNERABLE - Unsafe deserialization enables T1203
import pickle

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.data
    # T1203: Unsafe deserialization vulnerability
    obj = pickle.loads(data)  # Code execution risk
    return process_object(obj)

# DEFENDED - Safe deserialization
import json

@app.route('/api/data', methods=['POST'])  
def process_data():
    try:
        # T1203 Prevention: Safe JSON parsing
        data = json.loads(request.data)
        # Validate against schema
        if not validate_schema(data):
            return "Invalid data format", 400
        return process_object(data)
    except json.JSONDecodeError:
        return "Invalid JSON", 400
```

---

# <!-- fit --> Persistence & Session Hijacking

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1098 | Account Manipulation | Modifying user accounts for persistence |
| T1185 | Browser Session Hijacking | Stealing and reusing session tokens |
| T1505.003 | Web Shell | Server-side persistence mechanisms |


---

## Vulnerable Session Management

```javascript
// VULNERABLE - Weak session security enables T1185
const express = require('express');
const session = require('express-session');

app.use(session({
    secret: 'hardcoded-secret',  // T1552: Hardcoded secret
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false,        // T1185: No HTTPS requirement
        httpOnly: false,      // T1185: XSS vulnerable
        maxAge: 24 * 60 * 60 * 1000  // T1185: Long expiration
    }
}));

// No session validation or rotation
app.get('/api/data', (req, res) => {
    if (req.session.user) {
        return res.json(getData(req.session.user));
    }
    res.status(401).send('Unauthorized');
});
```

---

## Defended Session Management

```javascript
// DEFENDED - Secure session handling prevents T1185
const crypto = require('crypto');

app.use(session({
    secret: process.env.SESSION_SECRET,  // T1552 Prevention: Environment variable
    resave: false,
    saveUninitialized: false,
    rolling: true,  // T1185 Prevention: Session rotation
    cookie: {
        secure: true,     // T1185 Prevention: HTTPS only
        httpOnly: true,   // T1185 Prevention: XSS protection
        maxAge: 15 * 60 * 1000,  // T1185 Prevention: Short expiration
        sameSite: 'strict'       // CSRF protection
    }
}));

// T1185 Prevention: Session fingerprinting
function validateSession(req, res, next) {
    if (!req.session.user) return res.status(401).send('Unauthorized');
    
    const fingerprint = generateFingerprint(req);
    if (req.session.fingerprint !== fingerprint) {
        req.session.destroy();  // T1185 Detection: Session hijacking
        return res.status(401).send('Session security violation');
    }
    next();
}
```

---

## Web Shell Detection (T1505.003)

```csharp
// T1505.003 Detection: Web shell upload monitoring
public class FileUploadValidator
{
    private readonly string[] _suspiciousPatterns = {
        "eval(", "exec(", "system(", "passthru(",
        "<?php", "<%", "<script", "cmd.exe"
    };

    public bool ValidateUpload(IFormFile file)
    {
        // T1505.003 Prevention: File extension validation
        var allowedExtensions = new[] { ".jpg", ".png", ".pdf", ".docx" };
        var extension = Path.GetExtension(file.FileName).ToLower();
        
        if (!allowedExtensions.Contains(extension))
        {
            LogSecurityEvent("T1505.003", $"Suspicious extension: {extension}");
            return false;
        }
        
        // T1505.003 Detection: Content scanning
        using var reader = new StreamReader(file.OpenReadStream());
        var content = reader.ReadToEnd();
        
        foreach (var pattern in _suspiciousPatterns)
        {
            if (content.Contains(pattern, StringComparison.OrdinalIgnoreCase))
            {
                LogSecurityEvent("T1505.003", $"Web shell pattern detected: {pattern}");
                return false;
            }
        }
        
        return true;
    }
}
```

---

# <!-- fit --> Credential Access & Secrets

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1552 | Unsecured Credentials | Hardcoded secrets, config files |
| T1555 | Credentials from Password Stores | Browser/app credential extraction |
| T1528 | Steal Application Access Token | API tokens, OAuth tokens |


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


---

## Good Secrets Management - All Languages

```python
# PYTHON - GOOD: T1552 prevention
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# T1552 Prevention: Environment variables + Key Vault
DATABASE_URL = os.environ.get('DATABASE_URL')
credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.environ.get('KEY_VAULT_URL'), credential=credential)
API_KEY = client.get_secret("api-key").value
```

```csharp
// C# - GOOD: T1552 prevention
public class SecureConfig
{
    private readonly IConfiguration _config;
    
    public SecureConfig(IConfiguration config) => _config = config;
    
    // T1552 Prevention: Azure Key Vault integration
    public string ConnectionString => _config["KeyVault:ConnectionString"];
    public string ApiKey => _config["KeyVault:ApiKey"];
}
```

```javascript
// JAVASCRIPT - GOOD: T1552 prevention
require('dotenv').config();
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');

class SecureConfig {
    constructor() {
        this.secretClient = new SecretManagerServiceClient();
    }
    
    // T1552 Prevention: Google Secret Manager
    async getSecret(name) {
        const [version] = await this.secretClient.accessSecretVersion({
            name: `projects/${process.env.PROJECT_ID}/secrets/${name}/versions/latest`
        });
        return version.payload.data.toString();
    }
}
```

---

## Secrets Scanner Implementation

```python
# T1552 Prevention: Automated secrets detection
import re
import os

class SecretsScanner:
    def __init__(self):
        self.patterns = [
            (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded Password'),
            (r'api[_-]?key\s*[=:]\s*["\'][^"\']{16,}["\']', 'API Key'),
            (r'sk-[a-zA-Z0-9]{32,}', 'Secret Key'),
            (r'pk_live_[a-zA-Z0-9]{24,}', 'Live API Key'),
            (r'-----BEGIN [A-Z ]+-----', 'Private Key')
        ]
    
    def scan_file(self, filepath):
        violations = []
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                for pattern, description in self.patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        violations.append({
                            'file': filepath,
                            'line': content[:match.start()].count('\n') + 1,
                            'type': description,
                            'technique': 'T1552'
                        })
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
        
        return violations
```

---

# <!-- fit --> Defense Evasion & Log Tampering

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1027 | Obfuscated Files/Information | Hiding malicious content |
| T1070 | Indicator Removal on Host | Log deletion/tampering |
| T1036 | Masquerading | Appearing legitimate |


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
        # T1070: Log injection vulnerability
        logger.warning(f"Failed login for user: {username}")
        return "Invalid credentials", 401
    
    return "Login successful"

# Attack payload: "admin\n[INFO] Successful login for admin"
# Creates fake success log entry
```


---

## Tamper-Evident Logging (T1070 Prevention)

```csharp
// T1070 Prevention: Tamper-evident logging with hash chains
public class SecureLogger
{
    private string _lastHash = "genesis";
    private readonly IConfiguration _config;
    
    public void LogSecurityEvent(string technique, string details)
    {
        var logEntry = new SecurityLogEntry
        {
            Timestamp = DateTime.UtcNow,
            Technique = technique,
            Details = SanitizeInput(details),  // T1070 Prevention: Input sanitization
            PreviousHash = _lastHash
        };
        
        // T1070 Prevention: Cryptographic hash chain
        logEntry.Hash = ComputeHash($"{logEntry.Timestamp}{logEntry.Technique}{logEntry.Details}{_lastHash}");
        _lastHash = logEntry.Hash;
        
        // T1070 Prevention: Write to immutable storage
        WriteToImmutableStore(logEntry);
        
        // T1070 Prevention: Send to external SIEM
        await SendToSIEM(logEntry);
    }
    
    private string SanitizeInput(string input)
    {
        // Remove newlines and control characters that could enable log injection
        return Regex.Replace(input ?? "", @"[\r\n\t\f]", "_");
    }
}
```

---

## Immutable Logging Architecture

<div class="mermaid">
graph TD
    A[Application] --> B[Secure Logger]
    B --> C[Hash Validation]
    C --> D[Local Buffer]
    D --> E[Encrypted Storage]
    D --> F[External SIEM]
    D --> G[Blockchain Ledger]
    E --> H[Tamper Detection]
    F --> H
    G --> H
    H --> I[Alert Security Team]
</div>


---

# <!-- fit --> Supply Chain Compromise

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1195 | Supply Chain Compromise | Compromising upstream dependencies |
| T1195.001 | Compromise Software Dependencies | Malicious packages |


---

## Supply Chain Attack Examples

- **NPM**: `event-stream` package (2018) - 8M downloads, Bitcoin wallet stealer
- **PyPI**: Typosquatting attacks - `urllib3` vs `urllib4`  
- **NuGet**: Dependency confusion - internal vs public packages
- **Docker**: Compromised base images with embedded malware


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

---

## Package Integrity Validation

```python
# T1195.001 Prevention: Package integrity validation
import hashlib
import json

class PackageValidator:
    def __init__(self, lockfile_path):
        with open(lockfile_path) as f:
            self.lockfile = json.load(f)
    
    def validate_package(self, package_name, package_file):
        expected_hash = self.lockfile['packages'][package_name]['integrity']
        
        # T1195.001 Detection: Hash verification
        actual_hash = self.compute_package_hash(package_file)
        
        if actual_hash != expected_hash:
            self.log_security_event('T1195.001', {
                'package': package_name,
                'expected': expected_hash,
                'actual': actual_hash,
                'alert': 'Package integrity violation detected'
            })
            return False
            
        return True
    
    def compute_package_hash(self, package_file):
        hasher = hashlib.sha512()
        with open(package_file, 'rb') as f:
            hasher.update(f.read())
        return f"sha512-{hasher.hexdigest()}"
```

---

## Supply Chain Security Flow

<div class="mermaid">
flowchart TD
    A[Developer] --> B[Dependency Request]
    B --> C{Package Registry}
    C --> D[Integrity Check]
    D --> E{Hash Valid?}
    E -->|No| F[Block Installation]
    E -->|Yes| G[Vulnerability Scan]
    G --> H{Clean?}
    H -->|No| F
    H -->|Yes| I[Install Package]
    F --> J[Log T1195.001 Event]
    I --> K[Runtime Monitoring]
</div>


---

# <!-- fit --> Collection & Exfiltration

---

## Attacker Techniques

| Technique ID | Name | Description |
|--------------|------|-------------|
| T1213 | Data from Information Repositories | Bulk data access |
| T1567 | Exfiltration Over Web Service | Cloud storage uploads |
| T1020 | Automated Exfiltration | Scripted data theft |


---

## Data Access Anomaly Detection

```python
# T1213 Detection: Unusual data access patterns
class DataAccessMonitor:
    def __init__(self):
        self.user_baselines = {}
        
    def check_access_pattern(self, user_id, query, context):
        baseline = self.get_user_baseline(user_id)
        current_access = {
            'records_accessed': query.estimated_rows,
            'tables_accessed': len(query.tables),
            'time_of_day': context.timestamp.hour,
            'data_sensitivity': self.classify_sensitivity(query.tables)
        }
        
        # T1213 Detection: Statistical anomaly detection
        anomaly_score = self.calculate_anomaly_score(baseline, current_access)
        
        if anomaly_score > 0.8:  # High anomaly
            self.log_technique('T1213', {
                'user': user_id,
                'anomaly_score': anomaly_score,
                'query': query.sanitized_sql,
                'risk_factors': self.identify_risk_factors(current_access, baseline)
            })
            
            # T1213 Response: Require additional authentication
            return self.require_step_up_auth(user_id)
            
        return True
        
    def calculate_anomaly_score(self, baseline, current):
        # Z-score based anomaly detection
        scores = []
        for metric in ['records_accessed', 'tables_accessed']:
            z_score = abs((current[metric] - baseline[metric]['mean']) / baseline[metric]['std'])
            scores.append(min(z_score / 3.0, 1.0))  # Normalize to 0-1
        return max(scores)
```

---

## API Rate Limiting with Exfil Detection

```javascript
// T1567/T1020 Prevention: Exfiltration-aware rate limiting
class ExfiltrationDetector {
    constructor() {
        this.userTransferTracking = new Map();
    }
    
    async checkDataTransfer(userId, requestSize, responseSize) {
        const now = Date.now();
        const windowMs = 60 * 60 * 1000; // 1 hour window
        
        if (!this.userTransferTracking.has(userId)) {
            this.userTransferTracking.set(userId, []);
        }
        
        const transfers = this.userTransferTracking.get(userId);
        
        // Clean old transfers outside window
        const recentTransfers = transfers.filter(t => now - t.timestamp < windowMs);
        
        // Add current transfer
        recentTransfers.push({
            timestamp: now,
            responseSize,
            endpoint: request.path
        });
        
        this.userTransferTracking.set(userId, recentTransfers);
        
        // T1567/T1020 Detection: Bulk transfer analysis
        const totalTransferred = recentTransfers.reduce((sum, t) => sum + t.responseSize, 0);
        const transferRate = totalTransferred / (windowMs / 1000); // bytes per second
        
        if (totalTransferred > 100 * 1024 * 1024) { // 100MB in 1 hour
            await this.logSecurityEvent('T1567', {
                userId,
                totalTransferred,
                transferRate,
                requestCount: recentTransfers.length,
                timeWindow: '1h'
            });
            
            return false; // Block request
        }
        
        return true;
    }
}
```

---

## Data Flow Monitoring

<div class="mermaid">
graph TD
    A[User Request] --> B[Authentication]
    B --> C[Authorization]
    C --> D[Data Access Monitor]
    D --> E{Anomaly Detected?}
    E -->|Yes| F[T1213 Alert]
    E -->|No| G[Execute Query]
    G --> H[Response Size Check]
    H --> I{Bulk Transfer?}
    I -->|Yes| J[T1567 Alert]
    I -->|No| K[Rate Limit Check]
    K --> L{Exceeded?}
    L -->|Yes| M[T1020 Alert]
    L -->|No| N[Send Response]
    F --> O[Block / Throttle]
    J --> O
    M --> O
</div>


---

# DEMOS

---

# <!-- fit --> Practical Implementation

---

## ATT&CK-Informed Threat Modeling

<div class="mermaid">
flowchart TD
    A[Identify Application Feature] --> B[Map to ATT&CK Techniques]
    B --> C[Assess Risk & Impact]
    C --> D[Design Detection Controls]
    D --> E[Implement Monitoring]
    E --> F[Create Response Playbooks]
    F --> G[Test Against Techniques]
    G --> H[Monitor & Iterate]
    H --> B
</div>


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

---

## Building Detection Into Code

### Key Patterns:

- **Behavioral Analytics**: Monitor user patterns vs baselines
- **Technique Logging**: Tag events with ATT&CK IDs for correlation
- **Adaptive Controls**: Risk-based authentication and authorization  
- **Honey Tokens**: Fake data/accounts to detect unauthorized access
- **Immutable Auditing**: Tamper-evident logging and monitoring


---

## Defense in Depth Architecture

<div class="mermaid">
graph TB
    A1[Input Validation] --> A2[Authentication]
    A2 --> A3[Session Management]
    A3 --> A4[Authorization]
    A4 --> A5[Data Access Controls]
    A5 --> B1[Behavioral Analytics]
    B1 --> B2[Anomaly Detection]
    B2 --> B3[Technique Correlation]
    B3 --> B4[Threat Intelligence]
    B4 --> C1[Automated Blocking]
    C1 --> C2[Alert Generation]
    C2 --> C3[Investigation Workflows]
    C3 --> C4[Remediation Actions]
    A1 --> B1
</div>

---

## OWASP + ATT&CK Integration

<div class="mermaid">
flowchart LR
    A[Secure Coding] --> G[Secure by Design]
    D[Behavioral Monitoring] --> G
    B[Vulnerability Testing] --> H[Monitor by Behavior]
    E[Technique Correlation] --> H
    C[Security Reviews] --> I[Respond by Intelligence]
    F[Threat Hunting] --> I
    G --> H --> I
</div>


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

---

## Implementation Roadmap

### Phase 1 (Weeks 1-4): Foundation
- ✅ Map current features to ATT&CK techniques
- ✅ Implement secure logging with technique IDs
- ✅ Add basic behavioral analytics

### Phase 2 (Weeks 5-8): Detection
- ✅ Build anomaly detection for high-risk techniques
- ✅ Create automated response workflows
- ✅ Integrate with SIEM/security tools

### Phase 3 (Weeks 9-12): Advanced
- ✅ Implement honey tokens and deception
- ✅ Add threat intelligence correlation
- ✅ Build security dashboards and metrics

---

## Team Adoption Strategies

- **Training**: ATT&CK workshops for development teams
- **Process**: Include technique IDs in security requirements  
- **Tools**: Use ATT&CK Navigator for coverage visualization
- **Culture**: "Red team thinking" in design reviews
- **Metrics**: Track technique coverage and detection rates
- **Collaboration**: Regular sync between dev and security teams

---

## ATT&CK Navigator

- **Tool**: [mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)
- **Purpose**: Visualize technique coverage and gaps
- **Use Cases**: 
  - Map application defenses to techniques
  - Track security control effectiveness
  - Plan security improvements
  - Communicate risk to stakeholders

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

---

# <!-- fit --> Key Takeaways

---

## Key Takeaways

- ✅ **OWASP + ATT&CK = Complete Security** - Prevention + Detection
- ✅ **Think Like an Attacker** - Understand adversary behavior patterns  
- ✅ **Build Detection Into Code** - Monitoring isn't just ops responsibility
- ✅ **Log ATT&CK Technique IDs** - Enable security team correlation
- ✅ **Use Behavioral Analytics** - Go beyond simple rule-based detection
- ✅ **Start Small, Iterate** - Pick 3 techniques and expand coverage

---

<div class="columns">
<div>

## Links

- **[MITRE ATT&CK Framework](https://attack.mitre.org/)** - Main knowledge base
- **[ATT&CK for Enterprise](https://attack.mitre.org/matrices/enterprise/)** - Enterprise technique matrix  
- **[ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)** - Coverage visualization
- **[OWASP Developer Guide](https://owasp.org/www-project-developer-guide/)** - Secure development practices
- **[ATT&CK Evaluations](https://attackevals.mitre-engenuity.org/)** - Vendor capability assessments
- **[D3FEND](https://d3fend.mitre.org/)** - Defensive countermeasure knowledge base

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

---

# Questions?

![bg right](./img/owl.png)

<!-- Needed for mermaid, can be anywhere in file except frontmatter -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.2/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>
