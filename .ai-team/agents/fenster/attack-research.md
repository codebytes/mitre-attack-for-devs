# MITRE ATT&CK Framework: Comprehensive Developer Research

**Author:** Fenster (Security Researcher)  
**Date:** 2025-02-21  
**Purpose:** Deep-dive reference for developers building ATT&CK-aware applications

---

## 1. The 14 ATT&CK Tactics — Developer Relevance

### TA0043 - Reconnaissance
**Description:** Adversaries gather information to plan future operations.

**Why developers should care:** Poor error handling, verbose API responses, and exposed configuration files leak reconnaissance data. Information disclosure vulnerabilities (CWE-200) directly enable this tactic. Developers control what information surfaces to potential attackers through application behavior, documentation, and error messages.

**Top 3 Techniques:**
- **T1592 - Gather Victim Host Information**: Application error messages expose stack traces, framework versions, OS details. Defense: sanitize error responses, implement custom error pages.
- **T1595 - Active Scanning**: Attackers probe API endpoints, testing for authentication gaps. Defense: rate limiting, authentication on all endpoints, honeypot endpoints for detection.
- **T1589 - Gather Victim Identity Information**: Username enumeration through differential responses (timing, messages). Defense: consistent timing and messages for auth failures.

### TA0042 - Resource Development
**Description:** Adversaries establish resources to support operations.

**Why developers should care:** While mostly attacker-controlled infrastructure, developers can detect when their applications are being weaponized (compromised accounts creating infrastructure, API abuse for command-and-control). Monitoring for anomalous resource creation patterns and API usage is developer-implementable detection.

**Top 3 Techniques:**
- **T1583 - Acquire Infrastructure**: Compromised accounts creating cloud resources. Defense: require MFA for resource provisioning, alert on rapid resource creation.
- **T1587 - Develop Capabilities**: Attackers using your APIs to test malware. Defense: behavioral analytics on API usage patterns, sandbox suspicious activity.
- **T1608 - Stage Capabilities**: Using your storage/CDN to host malicious payloads. Defense: content scanning on uploads, integrity verification, access logging.

### TA0001 - Initial Access
**Description:** Adversaries attempt to enter your network/application.

**Why developers should care:** This is the front door. Every public-facing application component—web apps, APIs, webhooks—is a potential initial access vector. OWASP vulnerabilities (injection, broken auth) directly enable T1190 (Exploit Public-Facing Application). Authentication systems are the primary defense against T1078 (Valid Accounts) and T1110 (Brute Force).

**Top 3 Techniques:**
- **T1190 - Exploit Public-Facing Application**: SQL injection, command injection, deserialization flaws. Defense: parameterized queries, input validation, secure deserialization libraries.
- **T1078 - Valid Accounts**: Credential stuffing, password spraying with legitimate credentials. Defense: MFA, credential breach monitoring, behavioral analytics.
- **T1110 - Brute Force**: Automated password guessing, credential stuffing attacks. Defense: rate limiting, account lockout policies, CAPTCHA, leaked credential detection.

### TA0002 - Execution
**Description:** Adversaries run malicious code within the application or environment.

**Why developers should care:** Command injection (T1059), unsafe deserialization (T1203), and file inclusion vulnerabilities allow arbitrary code execution. Every place your code processes external input—API parameters, file uploads, template engines—is a potential execution vector. This is where injection flaws transition from vulnerability to active exploitation.

**Top 3 Techniques:**
- **T1059 - Command and Scripting Interpreter**: OS command injection via unsanitized inputs. Defense: parameterized commands, input allowlisting, avoid shell execution entirely.
- **T1203 - Exploitation for Client Execution**: Unsafe deserialization, template injection. Defense: safe deserialization libraries, sandboxed template engines, CSP headers.
- **T1204 - User Execution**: Tricking users into executing malicious content uploaded through your app. Defense: content scanning, file type restrictions, sandboxed preview, download warnings.

### TA0003 - Persistence
**Description:** Adversaries maintain access to systems after restarts, credential changes, or interruptions.

**Why developers should care:** Session management flaws (T1185), account manipulation capabilities (T1098), and web shell upload vulnerabilities (T1505.003) provide persistence. Every authentication token, session cookie, and user management endpoint is a persistence risk. Developers must design systems assuming attacker presence and implement detection for persistence mechanisms.

**Top 3 Techniques:**
- **T1098 - Account Manipulation**: Attackers modifying accounts to add backdoor access (email changes, privilege escalation). Defense: require re-authentication for account changes, audit log all modifications, alert on privilege changes.
- **T1185 - Browser Session Hijacking**: Stealing session tokens via XSS, lack of HttpOnly/Secure flags. Defense: HttpOnly/Secure/SameSite cookies, short session expiration, session fingerprinting.
- **T1505.003 - Web Shell**: Uploading server-side scripts for persistent backdoor access. Defense: file upload restrictions, content scanning, integrity monitoring, immutable infrastructure.

### TA0004 - Privilege Escalation
**Description:** Adversaries gain higher-level permissions.

**Why developers should care:** Broken access control (OWASP #1) directly enables privilege escalation. IDOR vulnerabilities (T1068), JWT manipulation (T1134), and role-based access control bypasses allow horizontal and vertical privilege escalation. Every authorization check is a privilege escalation boundary. Developers must verify not just authentication but also authorization for every sensitive operation.

**Top 3 Techniques:**
- **T1068 - Exploitation for Privilege Escalation**: IDOR vulnerabilities allowing access to other users' resources. Defense: verify resource ownership on every request, never trust client-provided IDs, implement RBAC correctly.
- **T1134 - Access Token Manipulation**: JWT algorithm confusion, claims tampering, token replay. Defense: strong signing algorithms (RS256, not none/HS256), validate all claims, verify issuer/audience, short expiration.
- **T1548 - Abuse Elevation Control Mechanism**: Bypassing permission checks through logic flaws. Defense: centralized authorization logic, fail-closed defaults, regular access control testing.

### TA0005 - Defense Evasion
**Description:** Adversaries avoid detection during their operation.

**Why developers should care:** Log injection (T1070), obfuscation, and tampering with audit trails directly undermine security monitoring. Developers control log integrity, input sanitization for logs, and whether logs are stored tamper-evidently. Without proper logging, all other detection fails. This tactic highlights the importance of treating logs as security-critical data requiring integrity protection.

**Top 3 Techniques:**
- **T1070 - Indicator Removal**: Log injection to corrupt/delete logs, preventing forensics. Defense: log input sanitization, immutable log storage (append-only), external SIEM forwarding, hash chains.
- **T1027 - Obfuscated Files or Information**: Hiding malicious payloads in uploads, encoding attacks. Defense: content scanning, deobfuscation before analysis, file integrity verification.
- **T1562 - Impair Defenses**: Disabling logging, rate limiting, or security features. Defense: tamper-proof configuration, alert on security control changes, require privileged access.

### TA0006 - Credential Access
**Description:** Adversaries steal account credentials.

**Why developers should care:** Hardcoded secrets (T1552), insecure credential storage (T1555), and credential dumping from memory/config files are developer-preventable. Every secret in code, config file, or environment variable is a credential access risk. This is where cryptographic failures (OWASP #2) intersect with attacker tactics. Secret management is foundational security hygiene.

**Top 3 Techniques:**
- **T1552 - Unsecured Credentials**: Hardcoded secrets in code, config files, environment variables. Defense: secrets management solutions (Key Vault, Secrets Manager), secret scanning in CI/CD, never commit secrets.
- **T1555 - Credentials from Password Stores**: Extracting credentials from browser storage, local databases. Defense: encrypt sensitive data at rest, use secure storage APIs, minimize client-side credential caching.
- **T1110 - Brute Force**: Credential stuffing, password spraying. Defense: rate limiting, account lockout, leaked credential checks, MFA.

### TA0007 - Discovery
**Description:** Adversaries explore the environment to understand what they can control.

**Why developers should care:** Username enumeration (T1087), API endpoint discovery (T1046), and information disclosure via error messages (T1082) help attackers map your application. Every differential response, verbose error, or predictable API structure aids discovery. Developers must design for opacity—consistent responses, minimal information disclosure, non-obvious API design.

**Top 3 Techniques:**
- **T1087 - Account Discovery**: Username enumeration via differential responses (timing, error messages, status codes). Defense: consistent responses for valid/invalid users, timing-constant operations, rate limiting.
- **T1046 - Network Service Discovery**: API endpoint enumeration, scanning for unprotected routes. Defense: authentication on all endpoints, remove server headers, API gateway with allowlisting, rate limiting.
- **T1082 - System Information Discovery**: Stack traces, framework versions, OS details from error messages. Defense: generic error messages in production, custom error pages, disable debug mode.

### TA0008 - Lateral Movement
**Description:** Adversaries move through your environment to reach their objectives.

**Why developers should care:** In microservices/cloud architectures, service-to-service communication without authentication (T1021), token reuse across services (T1550), and session hijacking enable lateral movement. Every internal API, message queue, or service mesh is a lateral movement path. Zero-trust architecture—authenticating every request even internally—is the developer's responsibility.

**Top 3 Techniques:**
- **T1021 - Remote Services**: Exploiting insecure service-to-service communication. Defense: mutual TLS (mTLS), service meshes with identity, authenticate all internal APIs, network segmentation.
- **T1550 - Use Alternate Authentication Material**: Reusing stolen tokens/cookies across services. Defense: scoped tokens per service, short-lived credentials, token binding, rotate secrets frequently.
- **T1563 - Remote Service Session Hijacking**: Taking over inter-service sessions. Defense: session binding to client identity, mutual authentication, detect token reuse anomalies.

### TA0009 - Collection
**Description:** Adversaries gather data of interest to their goal.

**Why developers should care:** Excessive data access permissions, lack of data access monitoring (T1213), and bulk export capabilities without controls enable collection. Developers design data access patterns and implement monitoring. If your app allows unrestricted bulk queries or doesn't monitor for anomalous data access, you're facilitating collection. Data loss prevention starts with access design.

**Top 3 Techniques:**
- **T1213 - Data from Information Repositories**: Bulk database queries, excessive API data retrieval. Defense: pagination limits, anomaly detection on access patterns, require justification for bulk access, audit logging.
- **T1005 - Data from Local System**: Attackers reading sensitive files/configs uploaded by users. Defense: encrypt data at rest, minimize data retention, access controls on file storage.
- **T1114 - Email Collection**: Compromised accounts accessing email via your application's integrations. Defense: OAuth scope limiting, detect bulk email access, alert on unusual patterns.

### TA0010 - Command and Control
**Description:** Adversaries communicate with compromised systems.

**Why developers should care:** While C2 is often network-layer, compromised applications can be used for C2 channels (WebSockets, legitimate APIs, covert channels in normal traffic). Detecting C2 requires monitoring for unusual communication patterns—beaconing, data exfiltration disguised as legitimate traffic. Developers can instrument applications to detect these patterns.

**Top 3 Techniques:**
- **T1071 - Application Layer Protocol**: Using HTTP/HTTPS APIs for C2 communication. Defense: behavioral analytics on API usage, detect beaconing patterns, anomalous user-agent strings, geolocation anomalies.
- **T1572 - Protocol Tunneling**: Tunneling C2 through WebSockets, legitimate protocols. Defense: deep packet inspection, monitor for unusual protocol usage, connection duration anomalies.
- **T1573 - Encrypted Channel**: C2 over encrypted channels. Defense: SSL/TLS inspection where appropriate, detect encrypted traffic to suspicious destinations, certificate pinning.

### TA0011 - Exfiltration
**Description:** Adversaries steal data from your environment.

**Why developers should care:** Exfiltration over web services (T1567)—cloud storage uploads, legitimate APIs—and automated exfiltration scripts (T1020) are application-layer concerns. Data loss prevention requires monitoring for bulk transfers, unusual upload patterns, and rate limiting. Every file upload endpoint and data export feature is an exfiltration vector requiring controls and monitoring.

**Top 3 Techniques:**
- **T1567 - Exfiltration Over Web Service**: Uploading stolen data to cloud storage, external APIs. Defense: outbound traffic monitoring, rate limiting on uploads, detect bulk transfers, DLP policies.
- **T1020 - Automated Exfiltration**: Scripted bulk data extraction. Defense: API rate limiting, anomaly detection on data access velocity, alert on automated patterns (user-agent, timing).
- **T1041 - Exfiltration Over C2 Channel**: Data sent via compromised application channels. Defense: monitor for unusual data volumes in outbound traffic, packet size anomalies, behavioral baselines.

### TA0040 - Impact
**Description:** Adversaries disrupt availability or integrity of systems and data.

**Why developers should care:** Application-layer DoS (T1499), data manipulation (T1565), and data destruction (T1485) are entirely developer-domain concerns. ReDoS vulnerabilities, lack of input validation causing resource exhaustion, and missing data integrity checks enable impact. Resilience and integrity verification must be designed into applications from the start.

**Top 3 Techniques:**
- **T1499 - Endpoint Denial of Service**: ReDoS via malicious regex, resource exhaustion attacks. Defense: input validation, regex timeout limits, rate limiting, async processing with queues, circuit breakers.
- **T1565 - Data Manipulation**: Tampering with data integrity without detection. Defense: HMAC/signature verification, audit trails, data integrity checks on read, cryptographic commitments.
- **T1485 - Data Destruction**: Malicious deletion or corruption of data. Defense: soft deletes, versioning, backup verification, require approval workflows, audit logging of deletions.

---

## 2. Developer-Centric Technique Deep Dives

### T1190 - Exploit Public-Facing Application
**What it is:** Exploiting vulnerabilities in web applications, APIs, or other internet-accessible services to gain unauthorized access or execute code. This is the primary initial access vector for most application attacks.

**How attackers use it:** SQL injection, command injection, deserialization flaws, path traversal, XXE, SSRF, and authentication bypasses are all T1190 techniques. Attackers scan for vulnerable applications using automated tools, exploit public vulnerability disclosures, and chain multiple weaknesses. Once a public-facing app is compromised, it provides the foothold for all subsequent attack phases.

**How developers defend:** Input validation and sanitization are foundational—never trust user input. Use parameterized queries for SQL, avoid shell execution, implement secure deserialization libraries (never pickle/yaml.load untrusted data), and validate/sanitize all API inputs. Keep frameworks and dependencies patched. Implement defense-in-depth: WAF, rate limiting, and security monitoring alongside secure coding. Regular penetration testing and SAST/DAST in CI/CD catch vulnerabilities before production.

### T1059 - Command and Scripting Interpreter
**What it is:** Executing system commands or scripts through application vulnerabilities, most commonly via command injection where user input is passed unsanitized to shell execution functions.

**How attackers use it:** Attackers inject shell metacharacters (`;`, `|`, `&&`, backticks) into inputs that are passed to system calls like `os.system()`, `exec()`, `eval()`, or template engines. Once command execution is achieved, attackers can read sensitive files, establish reverse shells, download additional payloads, or pivot to other systems. This technique often follows T1190 exploitation.

**How developers defend:** Avoid shell execution entirely when possible—use language-native libraries instead (e.g., file operations without `rm`). If shell execution is unavoidable, use parameterized commands or allowlists for inputs. Never concatenate user input into command strings. Implement strict input validation (allowlist known-good patterns), run processes with minimal privileges, and use sandboxing/containers to limit blast radius. Monitor for unusual process spawning.

### T1078 - Valid Accounts
**What it is:** Using legitimate credentials to gain access—whether stolen, leaked, purchased, or obtained via social engineering. Unlike exploitation, this technique leverages properly functioning authentication with compromised credentials.

**How attackers use it:** Credential stuffing (using breached password databases), phishing, password spraying, or purchasing credentials from dark web markets. Once valid credentials are obtained, attackers appear as legitimate users, bypassing many security controls. They can access data, modify configurations, or use the compromised account as a pivot point for further attacks.

**How developers defend:** Multi-factor authentication (MFA) is the strongest defense—credentials alone are insufficient. Monitor for credential stuffing patterns (login attempts with breached passwords, multiple account attempts from single IP). Implement rate limiting on login endpoints and account lockout policies. Use services like HaveIBeenPwned API or similar to check if user passwords are in known breach databases. Behavioral analytics can detect anomalous login patterns (unusual geolocation, device, timing).

### T1195 - Supply Chain Compromise
**What it is:** Compromising the development or distribution chain to inject malicious code into software dependencies, tools, or updates that victims will trust and integrate into their applications.

**How attackers use it:** Publishing malicious packages to npm/PyPI/NuGet with typosquatted names, compromising legitimate package maintainer accounts, backdooring open-source libraries, or injecting malicious code into build tools. The 2021 SolarWinds attack and 2022 event-stream npm incident exemplify this technique. Victims unknowingly integrate compromised dependencies, giving attackers widespread access.

**How developers defend:** Use dependency lock files (package-lock.json, requirements.txt with hashes) and verify package integrity. Enable dependency scanning tools (Dependabot, Snyk) to detect known vulnerabilities and suspicious packages. Pin dependencies to specific versions and audit updates carefully. Use private package registries for internal code. Implement Software Bill of Materials (SBOM) and signature verification for packages. Minimize dependencies overall—fewer dependencies mean smaller attack surface.

### T1552 - Unsecured Credentials
**What it is:** Storing credentials insecurely—hardcoded in source code, committed to repositories, stored in plaintext config files, or exposed in environment variables without proper protection.

**How attackers use it:** Attackers scan public GitHub repositories for hardcoded API keys, database credentials, and cloud access tokens using automated tools. They also compromise servers to read environment variables, config files, or memory dumps. Once credentials are obtained, attackers use them for T1078 (Valid Accounts) to access systems, databases, or cloud resources.

**How developers defend:** Never hardcode secrets in code—use secrets management solutions (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault, Google Secret Manager). Rotate secrets regularly and audit secret access. Implement secret scanning in CI/CD pipelines to prevent commits containing secrets (GitHub Advanced Security, GitGuardian, TruffleHog). Use short-lived credentials and least-privilege IAM policies. Encrypt configuration files and use environment-specific secret injection at runtime.

### T1070 - Indicator Removal on Host
**What it is:** Deleting or modifying logs, audit trails, and other forensic evidence to hide attacker activity and evade detection. Log injection attacks corrupt logs by inserting malicious entries or control characters.

**How attackers use it:** Attackers inject newline characters, ANSI escape sequences, or fake log entries into application inputs that are logged verbatim. This can corrupt log files, inject false entries to mislead investigators, or exploit log parsing vulnerabilities. Attackers also target log files for deletion or modification to remove traces of their activity. This technique is critical for maintaining stealth during long-term compromises.

**How developers defend:** Sanitize all inputs before logging—escape newlines, control characters, and special characters. Use structured logging (JSON) instead of freeform text logs to prevent injection. Send logs to immutable storage (append-only, write-once systems) or external SIEM immediately to prevent tampering. Implement cryptographic hash chains where each log entry includes a hash of the previous entry, making tampering detectable. Monitor for gaps in log sequences and alert on log integrity violations.

### T1110 - Brute Force
**What it is:** Automated attempts to guess credentials through password spraying (trying common passwords against many accounts), credential stuffing (using breached credentials), or traditional brute force (exhaustive password attempts).

**How attackers use it:** Attackers use botnets to distribute attempts across many IPs, evading simple rate limiting. They target accounts without MFA, use lists of breached passwords, and exploit predictable password patterns. Credential stuffing exploits password reuse across services. Once credentials are obtained, attackers use T1078 (Valid Accounts) for access.

**How developers defend:** Implement rate limiting on authentication endpoints (per IP, per account, globally). Use account lockout policies after repeated failures, but beware of lockout DoS attacks. Deploy CAPTCHA or proof-of-work challenges after failure thresholds. Check passwords against known breach databases (HaveIBeenPwned). Require MFA for all accounts. Monitor for distributed brute force patterns (many IPs targeting few accounts). Log authentication attempts for behavioral analysis.

### T1567 - Exfiltration Over Web Service
**What it is:** Uploading stolen data to external web services like cloud storage (Dropbox, Google Drive), file sharing sites, or legitimate APIs to exfiltrate data using normal-looking HTTPS traffic.

**How attackers use it:** Attackers leverage legitimate services to blend in with normal traffic, evading traditional DLP solutions. They automate bulk uploads using compromised credentials or API access. Data is often compressed or encrypted before upload to avoid content inspection. This technique follows T1213 (Data Collection) and is often automated with T1020 (Automated Exfiltration).

**How developers defend:** Implement outbound traffic monitoring and anomaly detection for large data transfers. Rate limit file uploads and API data exports. Monitor for bulk transfer patterns (large files, high velocity, unusual timing). Integrate DLP policies to scan outbound data for sensitive content. Require justification/approval workflows for bulk exports. Alert on uploads to known file-sharing services or unusual external IPs. Use behavioral baselines to detect unusual user activity.

### T1499 - Endpoint Denial of Service
**What it is:** Causing application unavailability through resource exhaustion, exploiting algorithmic complexity vulnerabilities like ReDoS (Regular Expression Denial of Service), or overwhelming rate limits.

**How attackers use it:** ReDoS exploits catastrophic backtracking in poorly designed regex patterns—attackers send crafted inputs that cause exponential processing time. Other techniques include triggering expensive operations (complex queries, large file processing), exhausting connection pools, or exploiting memory leaks. Unlike network-layer DDoS, this is application-layer and often requires fewer requests.

**How developers defend:** Audit regex patterns for complexity—avoid nested quantifiers and use non-backtracking engines. Implement input length limits before validation. Set timeouts on all operations (regex matching, database queries, external API calls). Use rate limiting and throttling at multiple levels (per user, per IP, globally). Implement circuit breakers and bulkheads to isolate failures. Use async processing with queues for expensive operations. Monitor resource utilization (CPU, memory, connections) and alert on anomalies.

### T1565 - Data Manipulation
**What it is:** Tampering with data integrity—modifying application data, configuration, or messages in transit or at rest without proper detection mechanisms to validate integrity.

**How attackers use it:** Attackers modify database records, API payloads, or configuration files to achieve their objectives—financial fraud (changing transaction amounts), privilege escalation (modifying role fields), or planting backdoors (altering code repositories). Without integrity verification, these modifications go undetected until impact occurs. This technique often follows T1068 (privilege escalation) or T1098 (account manipulation).

**How developers defend:** Implement HMAC or digital signatures for data integrity verification on sensitive data. Use cryptographic commitments—hash data and store hashes separately for later verification. Audit log all data modifications with who/what/when and make logs immutable. Implement data validation on read—verify checksums/signatures before trusting data. Use versioning and maintain historical records. Require approval workflows for critical data changes. Monitor for unexpected data modifications using behavioral analytics.

### T1098 - Account Manipulation
**What it is:** Modifying user accounts to maintain persistence or escalate privileges—adding MFA bypass, changing email addresses, modifying roles, or creating backdoor accounts.

**How attackers use it:** Attackers with initial access modify their own account or create new accounts with elevated privileges. They add secondary email addresses for password resets, disable MFA, or add SSH keys for persistent access. These modifications provide redundant access methods if primary credentials are revoked. This technique ensures persistence even if the initial access vector is closed.

**How developers defend:** Require re-authentication for sensitive account changes (email, password, MFA settings). Implement approval workflows for privilege escalation or role changes. Audit log all account modifications with detailed metadata (who, what, when, from where). Alert on privilege changes, new high-privilege accounts, or MFA modifications. Monitor for anomalous patterns (account creation bursts, off-hours privilege changes). Implement separation of duties—users cannot modify their own permissions.

### T1134 - Access Token Manipulation
**What it is:** Tampering with authentication tokens (JWT, OAuth, session tokens) to gain unauthorized access—modifying claims, exploiting algorithm confusion, replaying tokens, or forging signatures.

**How attackers use it:** JWT algorithm confusion attacks change `alg` header from RS256 to HS256, allowing signature verification with public key as HMAC secret. Attackers modify claims (user ID, roles) to escalate privileges. They replay captured tokens or extend expiration times. Weak signing secrets enable brute-force attacks to forge tokens. Once token is manipulated, attackers bypass authentication entirely.

**How developers defend:** Use strong asymmetric algorithms (RS256, ES256) and explicitly validate the algorithm—reject `none` algorithm. Validate all JWT claims: issuer (iss), audience (aud), expiration (exp), not-before (nbf). Verify claims against database—don't trust token alone for authorization. Use short-lived tokens (5-15 minutes) with refresh tokens. Implement token binding to client identity (IP, device fingerprint). Monitor for anomalous token usage patterns (geolocation changes, concurrent sessions).

### T1505.003 - Web Shell
**What it is:** Uploading malicious server-side scripts (PHP, JSP, ASPX) to compromised web servers, providing persistent remote access and command execution capability through HTTP requests.

**How attackers use it:** Attackers exploit file upload vulnerabilities to upload web shells disguised as legitimate files (images with embedded PHP, double extensions). Once deployed, web shells provide a backdoor for command execution, file access, database manipulation, and lateral movement. They blend with legitimate web traffic and persist across reboots. Famous examples include China Chopper and WSO web shells.

**How developers defend:** Restrict file upload types strictly—allowlist extensions and verify with content inspection, not just extension checking. Store uploaded files outside webroot with non-executable permissions. Scan uploads with antivirus/YARA rules for web shell patterns (eval, exec, base64_decode, system calls). Implement file integrity monitoring (FIM) to detect unauthorized file creation in web directories. Use immutable infrastructure where possible—containers that reset on deployment. Monitor for unusual web server process spawning.

### T1021 - Remote Services
**What it is:** Exploiting remote services for lateral movement—in cloud/microservices contexts, this means abusing service-to-service communication without proper authentication or authorization.

**How attackers use it:** In microservices architectures, internal APIs often trust the network perimeter, lacking authentication. Attackers who compromise one service can freely call other internal services. They exploit shared API keys used across services or lack of mTLS. This enables lateral movement through the application architecture, data access across services, and privilege escalation.

**How developers defend:** Implement zero-trust architecture—authenticate every service-to-service request regardless of network location. Use mutual TLS (mTLS) to verify both client and server identities. Issue scoped, short-lived service tokens with specific permissions. Implement service mesh (Istio, Linkerd) with identity and policy enforcement. Network segmentation to limit blast radius. Monitor for unusual service-to-service communication patterns. Require service accounts with least-privilege permissions.

### T1213 - Data from Information Repositories
**What it is:** Accessing and collecting large volumes of data from databases, APIs, or file repositories—often legitimate access used in unauthorized ways (excessive queries, bulk exports, unauthorized data access).

**How attackers use it:** Attackers with valid credentials (T1078) or API access use legitimate query capabilities to extract data at scale. They automate bulk queries, export entire databases, or use API endpoints to scrape data. The access appears legitimate but the volume and pattern are anomalous. This technique precedes T1567 (Exfiltration) and is often automated.

**How developers defend:** Implement anomaly detection on data access patterns—baseline normal query volumes and alert on statistical deviations. Use pagination limits and rate limiting on APIs. Monitor for bulk export operations and require justification or approval for large data requests. Implement data access auditing with user, timestamp, query details. Require step-up authentication (additional verification) for unusual access patterns. Use behavioral analytics to detect anomalous users (time of day, location, velocity).

---

## 3. OWASP Top 10 2025 → ATT&CK Mapping

| OWASP 2025 Category | ATT&CK Techniques | Explanation |
|---------------------|-------------------|-------------|
| **A01 - Broken Access Control** | T1078 (Valid Accounts), T1098 (Account Manipulation), T1068 (Privilege Escalation), T1134 (Access Token Manipulation) | IDOR, missing authorization checks, and privilege escalation flaws allow attackers to access unauthorized resources or elevate permissions |
| **A02 - Cryptographic Failures** | T1552 (Unsecured Credentials), T1555 (Credentials from Password Stores), T1565 (Data Manipulation) | Weak encryption, exposed secrets, and lack of integrity verification enable credential theft and data tampering |
| **A03 - Injection** | T1190 (Exploit Public-Facing Application), T1059 (Command Injection), T1189 (Drive-by Compromise) | SQL injection, command injection, and XSS enable initial access, code execution, and data exfiltration |
| **A04 - Insecure Design** | T1499 (Endpoint DoS), T1565 (Data Manipulation), T1213 (Data Collection) | Missing security controls, lack of rate limiting, and absence of data integrity checks enable various attack techniques |
| **A05 - Security Misconfiguration** | T1552 (Unsecured Credentials), T1082 (System Information Discovery), T1046 (Network Service Discovery) | Default credentials, verbose errors, and exposed admin interfaces enable reconnaissance and credential access |
| **A06 - Vulnerable and Outdated Components** | T1195 (Supply Chain Compromise), T1190 (Exploit Public-Facing Application) | Unpatched dependencies and compromised packages provide initial access vectors |
| **A07 - Identification and Authentication Failures** | T1110 (Brute Force), T1087 (Account Discovery), T1078 (Valid Accounts), T1185 (Session Hijacking) | Weak passwords, missing MFA, and session vulnerabilities enable unauthorized access |
| **A08 - Software and Data Integrity Failures** | T1195 (Supply Chain Compromise), T1565 (Data Manipulation), T1505.003 (Web Shell) | Lack of integrity verification enables supply chain attacks, data tampering, and malicious code deployment |
| **A09 - Security Logging and Monitoring Failures** | T1070 (Indicator Removal), T1562 (Impair Defenses) | Insufficient logging and missing alerting allow attackers to evade detection and remove evidence |
| **A10 - Server-Side Request Forgery (SSRF)** | T1090 (Proxy), T1572 (Protocol Tunneling), T1046 (Network Service Discovery) | SSRF enables internal network scanning, credential theft from metadata services, and pivoting to internal systems |

---

## 4. Modern Attack Chains

### Chain 1: Supply Chain to Persistence
1. **T1195.001** - Attacker publishes malicious npm package with typosquatted name (e.g., `requset` instead of `request`)
2. **T1059** - Package post-install script executes command to download second-stage payload
3. **T1552** - Script exfiltrates environment variables containing AWS credentials from developer workstation
4. **T1078** - Stolen AWS credentials used to access production cloud environment
5. **T1098** - Attacker creates backdoor IAM user with console access for persistence
6. **T1083** - Attacker enumerates S3 buckets to discover sensitive data stores
7. **T1567** - Exfiltrates customer data to external cloud storage using stolen credentials

### Chain 2: Initial Access to Data Breach
1. **T1190** - SQL injection vulnerability in public API endpoint allows authentication bypass
2. **T1078** - Attacker uses extracted admin credentials to login to application
3. **T1087** - Username enumeration reveals high-value accounts (executives, privileged users)
4. **T1098** - Attacker modifies own account to add admin role for privilege escalation
5. **T1213** - Bulk database queries extract customer PII and financial records
6. **T1560** - Data compressed and encrypted to evade DLP scanning
7. **T1567** - Exfiltrated via legitimate cloud storage API to attacker-controlled account

### Chain 3: Credential Stuffing to Lateral Movement
1. **T1110.004** - Credential stuffing attack using breached password database against login API
2. **T1078** - Successful login to compromised user account without MFA
3. **T1185** - Session hijacking via stolen session token lacking proper security flags
4. **T1550** - Stolen token reused across multiple microservices due to shared authentication
5. **T1021** - Lateral movement to internal admin API with no additional authentication
6. **T1098** - Creation of backdoor service account for persistent access
7. **T1213** - Access to internal data repositories and exfiltration of intellectual property

### Chain 4: File Upload to Web Shell Persistence
1. **T1190** - Unrestricted file upload vulnerability allows bypassing extension validation
2. **T1505.003** - Upload of PHP web shell disguised as image file with double extension
3. **T1059** - Web shell provides remote command execution on web server
4. **T1552** - Extraction of database credentials from application configuration files
5. **T1078** - Direct database access using stolen credentials, bypassing application logic
6. **T1565** - Modification of database records to inject malicious content into application
7. **T1485** - Ransomware deployment targeting database backups and production data

### Chain 5: API Abuse to Mass Exfiltration
1. **T1078** - Compromised API key obtained from public GitHub repository
2. **T1046** - API endpoint enumeration discovers unprotected bulk export functionality
3. **T1213** - Automated script executes mass data retrieval via pagination abuse
4. **T1020** - Scheduled task setup for continuous data collection over extended period
5. **T1567** - Gradual exfiltration to external API to evade volume-based detection
6. **T1070** - Log injection to mask exfiltration activity and corrupt audit trails
7. **T1485** - Data deletion after exfiltration to cause business impact

---

## 5. MITRE D3FEND Mappings

| Defensive Technique | D3FEND ID | Description |
|---------------------|-----------|-------------|
| Input Validation | D3-IVV | Validating and sanitizing inputs to prevent injection attacks (T1190, T1059) |
| Credential Hardening | D3-CH | Using secrets management and avoiding hardcoded credentials (T1552) |
| Multi-Factor Authentication | D3-MFA | Requiring additional verification factors beyond passwords (T1078, T1110) |
| Session Expiration | D3-SEAL | Implementing short-lived sessions to limit hijacking window (T1185) |
| Authentication Cache Invalidation | D3-ACI | Clearing cached credentials to prevent reuse (T1550) |
| Message Authentication | D3-MA | Using HMAC/signatures for data integrity (T1565) |
| File Analysis | D3-FA | Scanning uploaded files for malicious content (T1505.003) |
| Resource Access Pattern Analysis | D3-RAPA | Detecting anomalous data access patterns (T1213) |
| Outbound Traffic Filtering | D3-OTF | Monitoring and controlling data exfiltration (T1567) |
| Application Configuration Hardening | D3-ACH | Secure configuration to prevent information disclosure (T1082) |
| Identifier Activity Analysis | D3-IAA | Behavioral analytics on user/account activity (T1087, T1098) |
| Process Spawn Analysis | D3-PSA | Detecting unusual process creation patterns (T1059) |
| Certificate Analysis | D3-CA | Validating TLS certificates and detecting anomalies (T1021) |
| Network Traffic Filtering | D3-NTF | Controlling service-to-service communication (T1021) |
| Software Update | D3-SU | Keeping dependencies patched (T1195, T1190) |
| Strong Password Policy | D3-SPP | Enforcing password complexity and rotation (T1110) |
| File Integrity Monitoring | D3-FIM | Detecting unauthorized file modifications (T1505.003, T1565) |
| Log Retention | D3-LR | Immutable log storage to prevent tampering (T1070) |
| Rate Limiting | D3-RL | Controlling request velocity to prevent abuse (T1499, T1110) |
| Dead Code Elimination | D3-DCE | Removing unused dependencies to reduce attack surface (T1195) |

---

## 6. Emerging Techniques (2024-2026)

### AI/ML Security Threats
Large Language Model (LLM) injection attacks represent a new class of T1059-style exploitation where adversaries manipulate prompts to cause unintended AI behavior. Prompt injection can leak training data, bypass content filters, or cause the model to execute unauthorized actions. Model poisoning during training (analogous to T1195 supply chain compromise) can embed backdoors that activate on specific inputs. Adversarial examples can evade ML-based security controls like malware detection or authentication systems. Developers must treat LLM inputs/outputs as untrusted, implement prompt sanitization, validate AI responses before execution, and monitor for anomalous model behavior.

### Cloud-Native Attack Patterns
Container escape vulnerabilities enable T1068 privilege escalation from compromised containers to host systems. Kubernetes RBAC misconfigurations (overly permissive service accounts) enable T1078-style lateral movement across cluster resources. Cloud metadata service exploitation (IMDSv1 SSRF) provides T1552 credential access to IAM roles and secrets. Serverless function vulnerabilities (environment variable injection, dependency confusion) enable T1059 execution. Defense requires immutable infrastructure, network policies, Pod Security Standards, workload identity, and monitoring for unusual pod/container behavior.

### API-Specific Attacks
GraphQL-specific vulnerabilities include batching attacks for T1499 DoS, introspection abuse for T1046 discovery, and depth/complexity attacks for resource exhaustion. REST API parameter pollution and mass assignment enable T1068 privilege escalation. Broken object-level authorization (BOLA) at scale enables T1213 mass data collection. API key reuse across services facilitates T1550 lateral movement. Defense requires GraphQL query complexity limits, disable introspection in production, implement object-level authorization checks, scope API keys narrowly, and monitor for anomalous query patterns.

### Container and Orchestration Risks
Docker socket exposure enables full host compromise (T1068 privilege escalation). Privileged containers with host filesystem mounts provide T1552 credential access. Exposed Kubernetes dashboards and unauthenticated API servers enable T1078 unauthorized access. Image vulnerabilities and supply chain attacks (malicious base images) represent T1195 threats. Defense requires rootless containers, read-only filesystems, pod security policies, network segmentation, image scanning, admission controllers, and runtime security monitoring (Falco, Aqua).

### CI/CD Pipeline Targeting
Pipeline injection attacks (malicious pull requests executing code in CI) enable T1195 supply chain compromise. Stolen CI/CD credentials (GitHub Actions secrets, Jenkins credentials) provide T1552 access to production deployment pipelines. Compromised build artifacts (backdoored containers, malicious releases) enable widespread T1195 distribution. Dependency confusion attacks target private package registries. Defense requires protected branches, signed commits, separate build/deploy credentials, artifact signing and verification, SBOM generation, supply chain security tools (Sigstore, in-toto), and monitoring for unauthorized pipeline modifications.

---

**End of Research Document**
