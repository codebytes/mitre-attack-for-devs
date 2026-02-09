# MITRE ATT&CK for Developers - Python Code Samples

Educational code samples demonstrating common MITRE ATT&CK techniques and defensive measures. These samples are designed for security awareness training and show both vulnerable code patterns and secure implementations.

## ⚠️ Important Notice

**These samples are for educational purposes only.** They demonstrate security vulnerabilities and attack techniques to help developers understand threats and build better defenses. Do not use vulnerable code examples in production systems.

## Samples Overview

### 1. `credential_stuffing_detection.py`
**MITRE ATT&CK Technique:** T1110.004 - Credential Stuffing

Demonstrates detection and prevention of credential stuffing attacks where attackers use leaked username/password pairs to gain unauthorized access.

**Key Features:**
- Rate limiting per IP and per account
- Detection of automation patterns
- Account lockout and IP blocking
- Anomaly detection based on behavioral patterns

**Run:**
```bash
python3 credential_stuffing_detection.py
```

### 2. `command_injection.py`
**MITRE ATT&CK Technique:** T1059 - Command and Scripting Interpreter

Shows both vulnerable and secure implementations of command execution. Demonstrates how command injection works and how to prevent it.

**Key Features:**
- Vulnerable code using `os.system()` and `shell=True`
- Secure code using subprocess with argument lists
- Input validation and allowlisting
- Attack simulation and defense demonstration

**Run:**
```bash
python3 command_injection.py
```

### 3. `unsafe_deserialization.py`
**MITRE ATT&CK Technique:** T1059.006 - Execution via Deserialization

Demonstrates how insecure deserialization (especially with pickle) can lead to arbitrary code execution, and shows safe alternatives using JSON with schema validation.

**Key Features:**
- Vulnerable pickle deserialization
- Malicious payload demonstration
- Safe JSON-based alternative
- Schema validation and type checking

**Run:**
```bash
python3 unsafe_deserialization.py
```

### 4. `tamper_evident_logging.py`
**MITRE ATT&CK Technique:** T1070 - Indicator Removal on Host

Implements tamper-evident logging using cryptographic hash chains, making it detectable when logs are modified or deleted by attackers.

**Key Features:**
- Cryptographic hash chains for log integrity
- Detection of log tampering and deletion
- Verification function to validate log chain
- Export functionality for secure archival

**Run:**
```bash
python3 tamper_evident_logging.py
```

### 5. `data_access_monitor.py`
**MITRE ATT&CK Techniques:** 
- T1213 - Data from Information Repositories
- T1020 - Automated Exfiltration

Monitors data access patterns to detect anomalous behavior indicating data theft or exfiltration attempts.

**Key Features:**
- Baseline behavioral modeling
- Volume and velocity anomaly detection
- Time-based anomaly detection (unusual hours)
- Sensitivity-based access monitoring
- Rate limiting and alerting

**Run:**
```bash
python3 data_access_monitor.py
```

### 6. `secrets_scanner.py`
**MITRE ATT&CK Technique:** T1552 - Unsecured Credentials

Scans source code and configuration files for hardcoded credentials, API keys, passwords, and other secrets that attackers commonly search for.

**Key Features:**
- Pattern-based detection of various credential types
- Support for multiple file formats
- Severity classification
- False positive reduction
- Detailed reporting

**Run:**
```bash
python3 secrets_scanner.py
```

## Requirements

All samples use **only Python standard library** - no external dependencies required. Compatible with Python 3.7+.

## Educational Use

These samples are designed for:
- Security awareness training
- Developer education on secure coding
- Conference talks and presentations
- Understanding attacker techniques
- Learning defensive programming patterns

## Key Takeaways

### Defense-in-Depth Principles
1. **Input Validation**: Always validate and sanitize user input
2. **Least Privilege**: Run with minimum necessary permissions
3. **Defense Monitoring**: Implement behavioral monitoring and anomaly detection
4. **Secure Defaults**: Use safe APIs and configurations by default
5. **Layered Security**: Don't rely on a single defensive measure

### Common Patterns
- Use allowlists over denylists
- Implement rate limiting and throttling
- Log security-relevant events
- Monitor for anomalous behavior
- Use cryptographic verification where appropriate

## Additional Resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## License

These educational samples are provided as-is for learning purposes.

## Contributing

These samples are part of the "MITRE ATT&CK for Developers" conference talk. For questions or improvements, please refer to the main repository.

---

**Remember:** The best defense is understanding how attacks work and building security into your code from the start! 🛡️
