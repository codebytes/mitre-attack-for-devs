# ATT&CK Coverage Matrix — Quick Reference

**Last Updated:** 2026-02-22 by Kobayashi  
**Purpose:** Track technique coverage across slides and code samples

---

## Legend
- ✅ **Full** — Slides + vulnerable code + defended code + diagram
- 🟡 **Partial** — Slides exist but missing code/diagram elements
- 🔲 **Planned** — In P0/P1 backlog
- ❌ **Missing** — Not yet addressed

---

## Tactic Coverage Summary

| Tactic ID | Tactic Name | Status | Slides | Code Samples | Diagrams | Priority |
|-----------|-------------|--------|--------|--------------|----------|----------|
| TA0043 | Reconnaissance | 🔲 Planned | 1 slide (brief) | 0 | 0 | **P0-2** |
| TA0042 | Resource Development | 🔲 Planned | 1 slide (brief) | 0 | 0 | **P0-3** |
| TA0001 | Initial Access | ✅ Full | ~80 lines | 3 samples | 1 | Maintain |
| TA0002 | Execution | ✅ Full | ~100 lines | 3 samples | 1 | Maintain |
| TA0003 | Persistence | ✅ Full | ~90 lines | 2 samples | 1 | Maintain |
| TA0004 | Privilege Escalation | ✅ Full | ~80 lines | 2 samples | 1 | Maintain |
| TA0005 | Defense Evasion | ✅ Full | ~90 lines | 2 samples | 2 | Maintain |
| TA0006 | Credential Access | ✅ Full | ~130 lines | 3 samples | 1 | Maintain |
| TA0007 | Discovery | ✅ Full | ~90 lines | 2 samples | 1 | Maintain |
| TA0008 | Lateral Movement | ✅ Full | ~70 lines | 1 sample | 1 | Maintain |
| TA0009 | Collection | 🟡 Partial | ~120 lines | 2 samples | 1 | **P0-4** |
| TA0011 | Command & Control | 🔲 Planned | 1 slide (brief) | 0 | 0 | **P0-3** |
| TA0010 | Exfiltration | 🟡 Partial | (in Collection) | 1 sample | 1 | **P0-4** |
| TA0040 | Impact | 🟡 Partial | ~100 lines | 2 samples | 0 | **P0-1** |

**Totals**: 8 Full | 3 Partial | 3 Planned

---

## Technique-Level Coverage

### ✅ Initial Access (TA0001) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1190 | Exploit Public-Facing Application | ✅ | - | - | ✅ sql-injection.js |
| T1078 | Valid Accounts | ✅ | - | - | ✅ credential-stuffing-detection.js |
| T1110 | Brute Force | ✅ | ✅ credential_stuffing_detection.py | - | ✅ credential-stuffing-detection.js |
| T1566 | Phishing | ✅ (slide only) | - | - | - |

### ✅ Execution (TA0002) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1059 | Command & Scripting Interpreter | ✅ | ✅ command_injection.py | ✅ CommandInjection.cs | - |
| T1203 | Exploitation for Client Execution | ✅ | ✅ unsafe_deserialization.py | - | - |
| T1055 | Process Injection | ✅ (slide only) | - | - | - |

### ✅ Persistence (TA0003) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1098 | Account Manipulation | ✅ (slide only) | - | - | - |
| T1185 | Browser Session Hijacking | ✅ | - | ✅ SessionSecurity.cs | ✅ session-security.js |
| T1505.003 | Server Software Component: Web Shell | ✅ | - | ✅ WebShellDetection.cs | - |

### ✅ Privilege Escalation (TA0004) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1068 | Exploitation for Privilege Escalation (IDOR) | ✅ | ✅ (in slides) | - | - |
| T1548 | Abuse Elevation Control Mechanism | ✅ (slide only) | - | - | - |
| T1134 | Access Token Manipulation | ✅ | - | ✅ (in slides) | - |

### ✅ Defense Evasion (TA0005) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1027 | Obfuscated Files/Information | ✅ (slide only) | - | - | - |
| T1070 | Indicator Removal on Host | ✅ | ✅ tamper_evident_logging.py | ✅ TamperEvidentLogger.cs | - |
| T1036 | Masquerading | ✅ (slide only) | - | - | - |

### ✅ Credential Access (TA0006) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1552 | Unsecured Credentials | ✅ | ✅ secrets_scanner.py | ✅ SecretsManagement.cs | ✅ secrets-detection.js |
| T1555 | Credentials from Password Stores | ✅ (slide only) | - | - | - |
| T1528 | Steal Application Access Token | ✅ (slide only) | - | - | - |

### ✅ Discovery (TA0007) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1087 | Account Discovery | ✅ | ✅ (in slides) | - | - |
| T1046 | Network Service Scanning | ✅ | - | - | ✅ (in slides) |
| T1082 | System Information Discovery | ✅ (slide only) | - | - | - |

### ✅ Lateral Movement (TA0008) — FULL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1021 | Remote Services | ✅ | ✅ (in slides) | - | - |
| T1550 | Use Alternate Authentication Material | ✅ | ✅ (in slides) | - | - |
| T1563 | Remote Service Session Hijacking | ✅ (slide only) | - | - | - |

### 🟡 Collection (TA0009) — PARTIAL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1213 | Data from Information Repositories | ✅ | ✅ data_access_monitor.py | 🔲 **P0-4** | - |
| T1567 | Exfiltration Over Web Service | ✅ | - | - | ✅ data-exfiltration-detection.js |
| T1020 | Automated Exfiltration | ✅ | - | 🔲 **P0-4** | ✅ data-exfiltration-detection.js |
| T1030 | Data Transfer Size Limits | 🔲 **P0-4** | 🔲 | 🔲 | 🔲 |

### 🟡 Impact (TA0040) — PARTIAL
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1499 | Endpoint Denial of Service | ✅ | - | - | ✅ (in slides, ReDoS) |
| T1565 | Data Manipulation | ✅ | - | ✅ (in slides) | - |
| T1486 | Data Encrypted for Impact | ❌ → 🔲 **P0-1** | 🔲 | 🔲 | - |
| T1485 | Data Destruction | 🟡 (soft delete only) | 🔲 **P0-1** | ✅ (soft delete in slides) | - |

### 🔲 Reconnaissance (TA0043) — PLANNED (P0-2)
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1592 | Gather Victim Host Information | 🔲 | 🔲 | 🔲 | 🔲 |
| T1595 | Active Scanning | 🔲 | 🔲 | 🔲 | 🔲 |
| T1589 | Gather Victim Identity Information | 🔲 | 🔲 | - | 🔲 |

### 🔲 Command & Control (TA0011) — PLANNED (P0-3)
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1071 | Application Layer Protocol | 🔲 | 🔲 | - | 🔲 |
| T1572 | Protocol Tunneling | 🔲 | 🔲 | - | - |
| T1092 | Communication Through Removable Media | 🔲 | - | - | - |

### 🔲 Resource Development (TA0042) — PLANNED (P0-3)
| Technique | Name | Slides | Python | .NET | JavaScript |
|-----------|------|--------|--------|------|------------|
| T1583 | Acquire Infrastructure | 🔲 | - | - | 🔲 |
| T1584 | Compromise Infrastructure | 🔲 | - | - | 🔲 |

---

## Attack Chain Coverage (P1 Work)

| Chain Name | Techniques | Status | Priority |
|------------|-----------|--------|----------|
| Web App Takeover | T1190→T1059→T1505.003→T1021→T1213 | 🔲 P1-1 | High |
| Credential Compromise | T1566→T1078→T1098→T1087→T1550 | 🔲 P1-1 | High |
| Supply Chain Attack | T1195.001→T1203→T1070→T1027→T1567 | 🔲 P1-1 | High |
| Session Hijacking | T1185→T1068→T1213→T1020 | 🔲 P1-1 | Medium |
| Ransomware Kill Chain | T1190→T1059→T1552→T1486→T1499 | 🔲 P1-1 | High |

---

## Code Sample Inventory

### Python (6 samples)
- ✅ `command_injection.py` — T1059
- ✅ `credential_stuffing_detection.py` — T1110
- ✅ `data_access_monitor.py` — T1213
- ✅ `secrets_scanner.py` — T1552
- ✅ `tamper_evident_logging.py` — T1070
- ✅ `unsafe_deserialization.py` — T1203

### .NET (5 samples)
- ✅ `CommandInjection.cs` — T1059
- ✅ `SecretsManagement.cs` — T1552
- ✅ `SessionSecurity.cs` — T1185
- ✅ `TamperEvidentLogger.cs` — T1070
- ✅ `WebShellDetection.cs` — T1505.003

### JavaScript (6 samples)
- ✅ `credential-stuffing-detection.js` — T1110
- ✅ `data-exfiltration-detection.js` — T1567, T1020
- ✅ `secrets-detection.js` — T1552
- ✅ `session-security.js` — T1185
- ✅ `sql-injection.js` — T1190
- ✅ `supply-chain-verification.js` — T1195.001

**Total**: 17 samples across 3 languages

---

## P0 Work Items (Next 3 Weeks)

### P0-1: Complete Impact Section
- **Slides**: Add T1486 (ransomware) and T1485 (data destruction) examples
- **Code**: `python/ransomware_defense.py`, `dotnet/RansomwareDefense.cs`
- **Diagram**: Backup/recovery workflow with Mermaid

### P0-2: Build Reconnaissance Section
- **Slides**: T1592, T1595, T1589 with full examples
- **Code**: `python/reconnaissance_defense.py`, `dotnet/ReconnaissanceDefense.cs`, `javascript/reconnaissance-defense.js`
- **Diagram**: Metadata minimization architecture

### P0-3: Build Command & Control Section
- **Slides**: T1071, T1572 with detection examples
- **Code**: `python/c2_detection.py`, `javascript/c2-detection.js`
- **Diagram**: Egress monitoring decision tree

### P0-4: Complete Collection/Exfiltration
- **Slides**: T1030, T1041 examples
- **Code**: `dotnet/DataExfiltrationDetector.cs`
- **Diagram**: Data flow monitoring

---

**Next Review**: After P0 completion (Week 3)  
**Owner**: Kobayashi
