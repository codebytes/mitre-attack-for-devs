# MITRE ATT&CK for Developers — Python Code Samples

Educational samples demonstrating MITRE ATT&CK techniques and the defenses that
belong in application code.

## ⚠️ Important notice

**These samples are for educational purposes only.** They demonstrate
vulnerabilities alongside their defenses so developers can recognise both. Do not
use the vulnerable patterns in production.

## Scope: what belongs in your code

Credential stuffing, password spraying, impossible travel and device reputation
are handled by your **identity provider**, which observes sign-ins across every
application and tenant. A single application cannot see that context, so
reimplementing those detections produces a weaker control that also generates
false lockouts. Likewise, secret scanning is a solved problem — use GitHub Secret
Scanning with Push Protection, Gitleaks, or TruffleHog.

Those techniques are worth **monitoring**. They are not worth **rebuilding**.
These samples cover what is left: the boundaries only your application can enforce.

## Samples

### 1. `command_injection.py` — T1059
Command and Scripting Interpreter. Vulnerable `os.system()` and `shell=True`
versus `subprocess` with an argument list, plus input allowlisting and path
traversal prevention.

```bash
python3 command_injection.py
```

### 2. `unsafe_deserialization.py` — T1059.006
Execution via deserialization. Shows why `pickle.loads()` on untrusted bytes is
arbitrary code execution — the attacker's `__reduce__` runs during unpickling —
and the JSON-plus-schema-validation alternative.

```bash
python3 unsafe_deserialization.py
```

### 3. `bulk_export_guard.py` — T1213, T1567
Data from Information Repositories and Exfiltration Over Web Service. A fixed,
explainable export budget per role, decided *before* the query runs. Not an
anomaly score: a limit derived from the real workflow is testable, reviewable, and
can go in a runbook.

```bash
python3 bulk_export_guard.py
```

### 4. `tamper_evident_logging.py` — T1070
Indicator Removal. A cryptographic hash chain makes edits, deletions and
reordering detectable. Note the limitation documented in the module: a hash chain
proves *that* the local log changed, it does not prevent the change. Shipping
events off-host is what preserves the evidence.

```bash
python3 tamper_evident_logging.py
```

### 5. `data_integrity.py` — T1565
Data Manipulation. HMAC record signatures, a signed audit trail, mass-modification
detection and high-sensitivity field monitoring.

```bash
python3 data_integrity.py
```

## Requirements

Python 3.7+. Standard library only — no external dependencies.

## MITRE ATT&CK techniques covered

| Technique ID | Name | Sample File |
|-------------|------|-------------|
| T1059 | Command and Scripting Interpreter | `command_injection.py` |
| T1059.006 | Execution via Deserialization | `unsafe_deserialization.py` |
| T1213 | Data from Information Repositories | `bulk_export_guard.py` |
| T1567 | Exfiltration Over Web Service | `bulk_export_guard.py` |
| T1070 | Indicator Removal | `tamper_evident_logging.py` |
| T1565 | Data Manipulation | `data_integrity.py` |

### Monitored elsewhere, not reimplemented here

| Technique ID | Name | Where it belongs |
|-------------|------|------------------|
| T1110.003 | Password Spraying | Identity provider |
| T1110.004 | Credential Stuffing | Identity provider |
| T1552 | Unsecured Credentials | Secret scanning + push protection |

## Key takeaways

1. **Validate at the boundary.** Untrusted data must never reach a shell, a SQL
   parser, or a deserializer with its structure intact.
2. **Allowlist, never blocklist.** A blocklist has to be right every time; an
   allowlist only has to name what you accept.
3. **Bound the aggregate.** Individually-legal requests are what exfiltration
   looks like from inside an application.
4. **Decide before you execute.** Checking after the query runs means the data is
   already in memory.
5. **Log with technique IDs.** One denial is noise; a hundred is an attack, and
   only structured events make that visible.

## Additional resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
