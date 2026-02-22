# MITRE ATT&CK for Developers - JavaScript/Node.js Samples

Educational code samples demonstrating MITRE ATT&CK techniques and defenses for a conference talk. These samples are designed for security training and awareness.

## 📋 Overview

These samples demonstrate both **vulnerable** and **defended** code patterns for common attack techniques, following the MITRE ATT&CK framework.

## 🛡️ Samples

### 1. SQL Injection (`sql-injection.js`)
**ATT&CK Technique:** [T1190 - Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)

Demonstrates:
- ❌ **Vulnerable**: String concatenation in SQL queries
- ✅ **Defended**: Parameterized queries and input validation

```bash
node sql-injection.js
# Starts a web server on port 3000 with vulnerable and secure endpoints
```

### 2. Session Security (`session-security.js`)
**ATT&CK Technique:** [T1185 - Browser Session Hijacking](https://attack.mitre.org/techniques/T1185/)

Demonstrates:
- ❌ **Vulnerable**: Basic sessions without security controls
- ✅ **Defended**: Session fingerprinting, rotation, hijack detection, concurrent session limits

```bash
node session-security.js
# Shows session hijacking detection and prevention
```

### 3. Credential Stuffing Detection (`credential-stuffing-detection.js`)
**ATT&CK Technique:** [T1110.004 - Credential Stuffing](https://attack.mitre.org/techniques/T1110/004/)

Demonstrates:
- Rate limiting per IP and account
- Distributed attack detection (many accounts from one IP)
- Bot detection via timing analysis
- Automated blocking

```bash
node credential-stuffing-detection.js
# Simulates credential stuffing attacks and shows detection
```

### 4. Supply Chain Verification (`supply-chain-verification.js`)
**ATT&CK Technique:** [T1195.001 - Compromise Software Dependencies](https://attack.mitre.org/techniques/T1195/001/)

Demonstrates:
- Package-lock.json integrity verification
- Typosquatting detection (Levenshtein distance)
- Dangerous install script detection
- npm audit integration
- Dependency tree analysis

```bash
node supply-chain-verification.js
# Scans project for supply chain security issues
```

### 5. Data Exfiltration Detection (`data-exfiltration-detection.js`)
**ATT&CK Techniques:** 
- [T1567 - Exfiltration Over Web Service](https://attack.mitre.org/techniques/T1567/)
- [T1020 - Automated Exfiltration](https://attack.mitre.org/techniques/T1020/)

Demonstrates:
- Data volume tracking (per minute/hour/day)
- Bulk download detection
- Chunked exfiltration pattern detection
- Endpoint hopping detection
- Off-hours access monitoring

```bash
node data-exfiltration-detection.js
# Shows various data exfiltration patterns and detection
```

### 6. Secrets Detection (`secrets-detection.js`)
**ATT&CK Technique:** [T1552 - Unsecured Credentials](https://attack.mitre.org/techniques/T1552/)

Demonstrates:
- Scanning code for hardcoded secrets
- Pattern-based detection (API keys, tokens, passwords, connection strings)
- Entropy calculation for secret validation
- AWS, GitHub, Slack, Stripe, Google, and other service credentials

```bash
node secrets-detection.js
# Creates sample vulnerable file and scans for secrets
```

### 7. Authentication Monitoring (`auth-monitoring.js`)
**ATT&CK Technique:** [T1078 - Valid Accounts](https://attack.mitre.org/techniques/T1078/)

Demonstrates:
- Behavioral authentication monitoring
- Impossible travel detection (geolocation anomalies)
- Device fingerprint tracking
- Risk-based authentication decisions
- Privilege escalation monitoring
- Anomalous resource access detection

```bash
node auth-monitoring.js
# Shows detection of valid account misuse through behavioral analysis
```

### 8. Password Spray Detection (`password-spray-detection.js`)
**ATT&CK Technique:** [T1110.003 - Password Spraying](https://attack.mitre.org/techniques/T1110/003/)

Demonstrates:
- Cross-account password pattern detection
- Distributed spray attack detection (multiple IPs)
- Slow-and-low spray detection
- Progressive delays and IP blocking
- IP reputation tracking
- Timing analysis for bot detection

```bash
node password-spray-detection.js
# Simulates password spray attacks and shows detection mechanisms
```

### 9. Data Integrity Verification (`data-integrity.js`)
**ATT&CK Technique:** [T1565 - Data Manipulation](https://attack.mitre.org/techniques/T1565/)

Demonstrates:
- HMAC-based record integrity verification
- Tamper-evident audit trails
- Mass modification detection
- High-sensitivity field monitoring
- Modification velocity tracking
- Audit trail integrity verification

```bash
node data-integrity.js
# Shows data tampering detection and integrity verification
```

## 🎯 Key Features

All samples include:
- ✅ **Modern ES6+ JavaScript** (const/let, arrow functions, template literals)
- ✅ **Zero external dependencies** (only Node.js built-in modules)
- ✅ **JSDoc comments** with ATT&CK technique IDs
- ✅ **Educational structure** (vulnerable vs defended sections)
- ✅ **Example usage** with demonstrations
- ✅ **Comprehensive logging** for understanding attack patterns

## 🚀 Running the Samples

### Requirements
- Node.js 14+ (no npm packages needed!)

### Run Individual Samples
```bash
# Navigate to the samples directory
cd samples/javascript

# Run any sample
node sql-injection.js
node session-security.js
node credential-stuffing-detection.js
node supply-chain-verification.js
node data-exfiltration-detection.js
node secrets-detection.js
```

### Use as Modules
```javascript
// Import and use in your own code
const { CredentialStuffingDetector } = require('./credential-stuffing-detection.js');
const { SecretsDetector } = require('./secrets-detection.js');
const { SupplyChainVerifier } = require('./supply-chain-verification.js');

const detector = new CredentialStuffingDetector();
const result = detector.checkLoginAttempt('192.168.1.1', 'user@example.com');
console.log(result);
```

## 🔒 Security Notes

⚠️ **Educational Purpose Only**: These samples contain intentionally vulnerable code for educational purposes. **Never use vulnerable patterns in production code.**

### Best Practices Demonstrated:
1. **Input Validation**: Always validate and sanitize user input
2. **Parameterized Queries**: Never concatenate SQL queries
3. **Session Security**: Implement fingerprinting, rotation, and hijack detection
4. **Rate Limiting**: Protect against brute force and stuffing attacks
5. **Supply Chain Security**: Verify dependencies and detect typosquatting
6. **Data Loss Prevention**: Monitor and limit data transfers
7. **Secret Management**: Never hardcode credentials

## 📚 MITRE ATT&CK Techniques Covered

| Technique ID | Name | Sample File |
|-------------|------|-------------|
| T1190 | Exploit Public-Facing Application | `sql-injection.js` |
| T1185 | Browser Session Hijacking | `session-security.js` |
| T1110.004 | Credential Stuffing | `credential-stuffing-detection.js` |
| T1110.003 | Password Spraying | `password-spray-detection.js` |
| T1195.001 | Compromise Software Dependencies | `supply-chain-verification.js` |
| T1567 | Exfiltration Over Web Service | `data-exfiltration-detection.js` |
| T1020 | Automated Exfiltration | `data-exfiltration-detection.js` |
| T1552 | Unsecured Credentials | `secrets-detection.js` |
| T1078 | Valid Accounts | `auth-monitoring.js` |
| T1565 | Data Manipulation | `data-integrity.js` |

## 🎓 Learning Resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

## 📝 License

These samples are provided for educational purposes. Use responsibly and ethically.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve these educational samples!

---

**Remember**: Security is everyone's responsibility. Use these samples to learn, teach, and build more secure applications! 🛡️
