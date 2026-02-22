# Deep Dive Research Plan: MITRE ATT&CK Framework for Developers

**Decision Owner:** Kobayashi  
**Date:** 2026-02-22  
**Status:** Proposed

---

## Executive Summary

This research plan defines a structured expansion of the existing MITRE ATT&CK for Developers content. Current slides cover 11 of 14 ATT&CK tactics with solid code examples across 3 languages, but gaps exist in both technique depth and cross-tactic attack chain narratives. This plan prioritizes closing critical gaps, expanding technique coverage, and building realistic multi-stage attack scenarios.

---

## A. Current Coverage Audit

### ✅ **FULLY COVERED** (8 tactics with complete code examples + diagrams)

1. **Initial Access** (TA0001) — T1190, T1078, T1110, T1566
   - SQL injection, credential stuffing, valid accounts
   - Code samples: Python, JavaScript
   - Diagrams: ✅

2. **Execution** (TA0002) — T1059, T1203, T1055
   - Command injection, unsafe deserialization, client execution
   - Code samples: Python, .NET, JavaScript
   - Diagrams: ✅

3. **Persistence** (TA0003) — T1098, T1185, T1505.003
   - Session hijacking, web shells, account manipulation
   - Code samples: .NET, JavaScript
   - Diagrams: ✅

4. **Privilege Escalation** (TA0004) — T1068, T1548, T1134
   - IDOR, token manipulation, access control bypass
   - Code samples: Python, .NET
   - Diagrams: ✅

5. **Credential Access** (TA0006) — T1552, T1555, T1528
   - Hardcoded secrets, Key Vault integration, secrets scanning
   - Code samples: Python, .NET, JavaScript
   - Diagrams: ✅

6. **Defense Evasion** (TA0005) — T1027, T1070, T1036
   - Log injection, tamper-evident logging, log integrity
   - Code samples: Python, .NET
   - Diagrams: ✅ (Immutable Logging Architecture)

7. **Discovery** (TA0007) — T1087, T1046, T1082
   - User enumeration, API endpoint scanning, info disclosure
   - Code samples: Python, JavaScript
   - Diagrams: ✅

8. **Lateral Movement** (TA0008) — T1021, T1550, T1563
   - Service-to-service auth, mTLS, token reuse
   - Code samples: Python
   - Diagrams: ✅

### 🟡 **PARTIALLY COVERED** (3 tactics with technique lists but incomplete code/defense examples)

9. **Collection** (TA0009) — T1213, T1567, T1020
   - Data access anomaly detection: ✅ (Python)
   - Exfiltration detection: ✅ (JavaScript)
   - **GAPS**: Missing .NET examples, no code for T1030 (Data Transfer Size Limits), no diagrams for detection workflow

10. **Impact** (TA0040) — T1499, T1565, T1486, T1485
   - ReDoS prevention: ✅ (JavaScript)
   - Data integrity: ✅ (C#)
   - **GAPS**: No examples for T1486 (ransomware-style encryption detection), T1485 needs more depth (backup verification, recovery workflows)

11. **Supply Chain Compromise** (TA0043 sub-tactic under TA0001) — T1195, T1195.001
   - Package verification: ✅ (NPM, Python, NuGet)
   - Integrity validation: ✅ (JavaScript)
   - **GAPS**: No container image security, no SBOM generation examples, no CI/CD pipeline hardening

### ❌ **MISSING** (3 tactics with minimal or no coverage)

12. **Reconnaissance** (TA0043) — T1592, T1595 (brief mention only)
   - Current: Single slide listing developer responsibilities
   - **NEEDED**: Code examples for error sanitization, debug endpoint removal, metadata minimization, API fingerprinting prevention

13. **Resource Development** (TA0042) — T1583, T1584 (brief mention only)
   - Current: Dismissed as "largely outside developer control"
   - **NEEDED**: Webhook validation, third-party integration verification, infrastructure-as-code security

14. **Command & Control** (TA0011) — T1071, T1572 (brief mention only)
   - Current: Single slide listing developer responsibilities
   - **NEEDED**: WebSocket abuse detection, covert channel prevention, DNS tunneling detection, egress filtering patterns

---

## B. Gap Analysis

### **Critical Gaps (Blocking Complete Coverage)**

1. **Incomplete Impact Tactics**
   - Slides end with technique table at line 1194 but lack:
     - Ransomware defense patterns (T1486)
     - Data destruction recovery (T1485)
     - Application-level DoS beyond ReDoS (T1499 broader coverage)

2. **Shallow Reconnaissance Coverage**
   - No code examples for preventing attacker reconnaissance
   - Missing: Error message sanitization, version header removal, API enumeration prevention

3. **Command & Control Blind Spot**
   - Developers absolutely CAN influence C2 detection (WebSocket monitoring, DNS tunneling detection)
   - Zero code examples for detecting unusual outbound connections

4. **Missing Multi-Stage Attack Scenarios**
   - Current slides treat techniques in isolation
   - Need realistic attack chains showing how techniques combine (e.g., T1190→T1059→T1505.003→T1021)

### **Secondary Gaps (Expansion Opportunities)**

5. **Code Sample Language Imbalance**
   - Python: 6 samples
   - .NET: 5 samples
   - JavaScript: 6 samples
   - **Gap**: Some tactics only have 1 language example

6. **Missing Advanced Scenarios**
   - No GraphQL-specific attack examples (T1190, T1087)
   - No gRPC security patterns (T1021)
   - No serverless/FaaS-specific defenses (T1190, T1078)

7. **Diagram Gaps**
   - No comprehensive "attack chain" diagrams showing tactic progression
   - Missing: Detection decision trees for high-risk techniques
   - Missing: Defense-in-depth architecture per tactic

---

## C. Prioritized Research Backlog

### **P0: Critical — Complete Existing Coverage (2-3 weeks)**

| ID | Task | Techniques | Deliverables |
|----|------|-----------|--------------|
| P0-1 | Complete Impact section | T1486, T1485, T1499 | 3-4 slides with code examples (Python, .NET), Mermaid diagram for backup/recovery workflow |
| P0-2 | Expand Reconnaissance | T1592, T1595, T1589 | 4-5 slides with code examples (all languages), diagram for metadata minimization architecture |
| P0-3 | Build out Command & Control | T1071, T1572, T1092 | 4-5 slides with detection code (Python, JavaScript), diagram for egress monitoring |
| P0-4 | Fill Collection/Exfiltration gaps | T1030, T1041 | 2-3 slides with .NET examples, data flow monitoring diagram |

**Estimated Output**: +20 slides, +8 code samples, +4 Mermaid diagrams

---

### **P1: Important — Attack Chains & Advanced Techniques (3-4 weeks)**

| ID | Task | Techniques | Deliverables |
|----|------|-----------|--------------|
| P1-1 | Multi-stage attack scenarios | Cross-tactic chains | 5-6 slides with end-to-end attack narratives, Mermaid sequence diagrams |
| P1-2 | GraphQL security patterns | T1190, T1087, T1213 | 3-4 slides, code samples (JavaScript, Python) |
| P1-3 | Serverless/FaaS defenses | T1078, T1190, T1552 | 3-4 slides, code samples (Python, JavaScript) |
| P1-4 | Container security | T1195, T1610 | 3-4 slides, Dockerfile examples, supply chain diagrams |
| P1-5 | gRPC/microservices security | T1021, T1550 | 2-3 slides, code samples (.NET, Python) |

**Attack Chain Priorities** (see Section E for details):
1. **Web App Takeover**: T1190 → T1059 → T1505.003 → T1021 → T1213
2. **Credential Compromise**: T1566 → T1078 → T1098 → T1087 → T1550
3. **Supply Chain Attack**: T1195.001 → T1203 → T1070 → T1027 → T1567
4. **Session Hijacking to Exfil**: T1185 → T1068 → T1213 → T1020
5. **Ransomware Kill Chain**: T1190 → T1059 → T1552 → T1486 → T1499

**Estimated Output**: +20 slides, +10 code samples, +6 Mermaid diagrams

---

### **P2: Nice-to-Have — Ecosystem Expansion (4-5 weeks)**

| ID | Task | Techniques | Deliverables |
|----|------|-----------|--------------|
| P2-1 | Add Go code samples | T1059, T1021, T1552 | 5-6 samples in `samples/go/` |
| P2-2 | Add Rust code samples | T1059, T1552, T1565 | 4-5 samples in `samples/rust/` |
| P2-3 | Mobile-specific techniques | T1516, T1517, T1428 | 3-4 slides, Swift/Kotlin examples |
| P2-4 | CI/CD pipeline security | T1195.001, T1525 | 3-4 slides, GitHub Actions/GitLab CI examples |
| P2-5 | Advanced detection ML models | T1078, T1110, T1213 | 2-3 slides, scikit-learn examples |

**Estimated Output**: +15 slides, +15 code samples (new languages)

---

## D. Content Architecture

### **Proposed Slide Structure Expansion**

```
Current Structure (1531 lines):
├── Introduction (lines 1-150)
├── Tactic Coverage (lines 151-1280)
├── Other Tactics Brief (lines 1281-1310)
├── DEMOS placeholder (line 1313)
├── Practical Implementation (lines 1316-1477)
└── Conclusion (lines 1478-1531)

Proposed Expanded Structure (~2200 lines):
├── Introduction (unchanged)
├── Tactic Coverage - EXPANDED
│   ├── [Existing 11 tactics] (lines 151-1280)
│   ├── Reconnaissance - FULL SECTION (+100 lines)
│   ├── Command & Control - FULL SECTION (+100 lines)
│   ├── Resource Development - FULL SECTION (+80 lines)
│   └── Impact - COMPLETE (+60 lines, extend existing)
├── Attack Chain Scenarios - NEW SECTION (+200 lines)
│   ├── Scenario 1: Web App Takeover
│   ├── Scenario 2: Credential Compromise
│   ├── Scenario 3: Supply Chain Attack
│   ├── Scenario 4: Session Hijacking to Exfil
│   └── Scenario 5: Ransomware Kill Chain
├── DEMOS (unchanged)
├── Practical Implementation - EXPANDED (+150 lines)
│   ├── [Existing content]
│   ├── ATT&CK Technique Coverage Matrix - NEW
│   ├── Detection Engineering Patterns - NEW
│   └── Testing & Validation - NEW
└── Conclusion (unchanged)
```

### **Code Sample Organization**

```
samples/
├── python/
│   ├── [existing 6 files]
│   ├── reconnaissance_defense.py       # P0-2 (NEW)
│   ├── c2_detection.py                 # P0-3 (NEW)
│   ├── graphql_security.py             # P1-2 (NEW)
│   ├── serverless_defense.py           # P1-3 (NEW)
│   └── ransomware_defense.py           # P0-1 (NEW)
├── dotnet/
│   ├── [existing 5 files]
│   ├── DataExfiltrationDetector.cs     # P0-4 (NEW)
│   ├── RansomwareDefense.cs            # P0-1 (NEW)
│   ├── GrpcSecurity.cs                 # P1-5 (NEW)
│   └── ReconnaissanceDefense.cs        # P0-2 (NEW)
├── javascript/
│   ├── [existing 6 files]
│   ├── c2-detection.js                 # P0-3 (NEW)
│   ├── graphql-security.js             # P1-2 (NEW)
│   ├── serverless-defense.js           # P1-3 (NEW)
│   └── reconnaissance-defense.js       # P0-2 (NEW)
├── go/ (P2-1 - future)
│   └── [5-6 key technique samples]
└── rust/ (P2-2 - future)
    └── [4-5 key technique samples]
```

### **Mermaid Diagram Strategy**

**New Diagrams Needed**:

1. **Backup & Recovery Workflow** (P0-1, T1486/T1485)
   ```
   graph: Data → Backup → Verification → Recovery → Validation
   ```

2. **Reconnaissance Defense Architecture** (P0-2, T1592/T1595)
   ```
   flowchart: Request → Error Sanitizer → Version Stripper → Response
   ```

3. **Egress Monitoring Decision Tree** (P0-3, T1071/T1572)
   ```
   flowchart: Outbound Request → Protocol Analysis → Anomaly? → Block/Alert
   ```

4. **Data Exfiltration Detection Pipeline** (P0-4, T1030/T1041)
   ```
   graph: User Activity → Transfer Analysis → Threshold Check → Alert
   ```

5. **Attack Chain Sequence Diagrams** (P1-1, 5 scenarios)
   ```
   sequenceDiagram: Attacker → App → Database → Lateral Service → Exfil
   ```

6. **Detection Engineering Pipeline** (P1 - Practical Implementation)
   ```
   flowchart: Technique Mapping → Detection Logic → Alert Tuning → Response Automation
   ```

---

## E. Cross-References: Realistic Attack Chains

### **Attack Chain 1: Web Application Takeover**
**Narrative**: Attacker exploits a public API, executes commands, installs a web shell, moves laterally, and steals data.

| Stage | Tactic | Technique | Code Example Location |
|-------|--------|-----------|----------------------|
| 1. Initial breach | Initial Access | T1190 (SQL Injection) | `javascript/sql-injection.js` |
| 2. Code execution | Execution | T1059 (Command Injection) | `dotnet/CommandInjection.cs` |
| 3. Persistence | Persistence | T1505.003 (Web Shell) | `dotnet/WebShellDetection.cs` |
| 4. Lateral movement | Lateral Movement | T1021 (Service-to-Service) | `python/service_auth.py` (NEW) |
| 5. Data theft | Collection | T1213 (Data Access) | `python/data_access_monitor.py` |

**Mermaid Diagram**: Sequence diagram showing attacker progression through kill chain with detection points highlighted.

---

### **Attack Chain 2: Credential Compromise to Account Takeover**
**Narrative**: Phishing leads to valid account access, privilege escalation, user enumeration, and lateral movement.

| Stage | Tactic | Technique | Code Example Location |
|-------|--------|-----------|----------------------|
| 1. Social engineering | Initial Access | T1566 (Phishing) | [Detection pattern in slides] |
| 2. Valid account use | Initial Access | T1078 (Valid Accounts) | `javascript/credential-stuffing-detection.js` |
| 3. Account manipulation | Persistence | T1098 (Account Manipulation) | `dotnet/SessionSecurity.cs` |
| 4. User enumeration | Discovery | T1087 (Account Discovery) | `python/user_enumeration.py` (NEW) |
| 5. Token reuse | Lateral Movement | T1550 (Alternate Auth) | `dotnet/session_security.cs` (expand) |

**Mermaid Diagram**: Flowchart showing credential lifecycle and detection opportunities.

---

### **Attack Chain 3: Supply Chain Compromise**
**Narrative**: Malicious package leads to client-side execution, log tampering, obfuscation, and data exfiltration.

| Stage | Tactic | Technique | Code Example Location |
|-------|--------|-----------|----------------------|
| 1. Malicious dependency | Initial Access | T1195.001 (Compromised Dependency) | `javascript/supply-chain-verification.js` |
| 2. Client-side execution | Execution | T1203 (Client Execution) | `python/unsafe_deserialization.py` |
| 3. Log tampering | Defense Evasion | T1070 (Indicator Removal) | `python/tamper_evident_logging.py` |
| 4. Obfuscation | Defense Evasion | T1027 (Obfuscated Files) | [Detection pattern in slides] |
| 5. Data exfiltration | Exfiltration | T1567 (Web Service) | `javascript/data-exfiltration-detection.js` |

**Mermaid Diagram**: Supply chain flow with verification checkpoints and failure modes.

---

### **Attack Chain 4: Session Hijacking to Data Exfiltration**
**Narrative**: Session token theft leads to privilege escalation, data access, and automated exfiltration.

| Stage | Tactic | Technique | Code Example Location |
|-------|--------|-----------|----------------------|
| 1. Session theft | Persistence | T1185 (Session Hijacking) | `dotnet/SessionSecurity.cs` |
| 2. Privilege escalation | Privilege Escalation | T1068 (IDOR) | `python/idor_defense.py` (NEW) |
| 3. Data access | Collection | T1213 (Data Collection) | `python/data_access_monitor.py` |
| 4. Automated exfil | Exfiltration | T1020 (Automated Exfiltration) | `javascript/data-exfiltration-detection.js` |

**Mermaid Diagram**: Session lifecycle with hijacking detection and response flow.

---

### **Attack Chain 5: Ransomware Kill Chain**
**Narrative**: Web exploit leads to command execution, credential theft, data encryption, and denial of service.

| Stage | Tactic | Technique | Code Example Location |
|-------|--------|-----------|----------------------|
| 1. Initial breach | Initial Access | T1190 (Exploit Public-Facing) | `javascript/sql-injection.js` |
| 2. Command execution | Execution | T1059 (Command Injection) | `python/command_injection.py` |
| 3. Credential theft | Credential Access | T1552 (Unsecured Credentials) | `python/secrets_scanner.py` |
| 4. Data encryption | Impact | T1486 (Data Encrypted for Impact) | `python/ransomware_defense.py` (NEW) |
| 5. Denial of service | Impact | T1499 (Endpoint DoS) | `javascript/redos_defense.js` (expand) |

**Mermaid Diagram**: Ransomware attack timeline with backup/recovery intervention points.

---

## F. Research Methodology

### **Phase 1: Gap Closure (P0 - Weeks 1-3)**
1. **Week 1**: Research & outline P0 sections (Reconnaissance, C2, Impact completion)
2. **Week 2**: Write code samples for all P0 tasks (12 new samples across 3 languages)
3. **Week 3**: Create slides, diagrams, and integrate into main deck

**Deliverables**:
- 20 new slides
- 8 code samples
- 4 Mermaid diagrams
- Updated slide deck at ~1750 lines

---

### **Phase 2: Attack Chains & Advanced Techniques (P1 - Weeks 4-7)**
1. **Week 4**: Design 5 attack chain scenarios with narrative structure
2. **Week 5**: Build attack chain slides with sequence diagrams
3. **Week 6**: Develop GraphQL, serverless, and container security content
4. **Week 7**: Write code samples and integrate into deck

**Deliverables**:
- 20 new slides (5 attack chains + 15 advanced techniques)
- 10 code samples
- 6 Mermaid diagrams
- Updated slide deck at ~2050 lines

---

### **Phase 3: Ecosystem Expansion (P2 - Weeks 8-12, Optional)**
1. **Weeks 8-9**: Add Go code samples (5-6 samples)
2. **Weeks 10-11**: Add Rust code samples (4-5 samples)
3. **Week 12**: Mobile, CI/CD, and ML detection content

**Deliverables**:
- 15 new slides
- 15 code samples (new languages)
- Updated slide deck at ~2200 lines

---

## G. Success Metrics

### **Coverage Metrics**
- **Tactic Coverage**: 14/14 tactics with full sections (currently 11/14)
- **Technique Coverage**: 50+ techniques with code examples (currently ~30)
- **Language Balance**: All P0/P1 techniques have examples in 2+ languages
- **Diagram Coverage**: 15+ Mermaid diagrams (currently ~8)

### **Quality Metrics**
- Every technique includes: Vulnerable code + Defended code + Detection logic
- Every attack chain maps to 5+ existing/new code samples
- All code samples run without errors, include ATT&CK IDs in comments
- All diagrams render correctly in Marp

### **Adoption Metrics** (Post-Launch)
- GitHub stars, forks, issues (community engagement)
- Presentation feedback scores
- Blog post shares, conference submissions accepted

---

## H. Risk Assessment

### **Research Risks**
1. **Scope Creep**: Attack chains could expand indefinitely
   - **Mitigation**: Limit to 5 scenarios, cap at 200 slides total
2. **Code Sample Complexity**: Advanced techniques may be hard to demo safely
   - **Mitigation**: Use mock/simulation code, not actual exploits
3. **Maintenance Burden**: More code = more to maintain as libraries evolve
   - **Mitigation**: Focus on patterns over specific library versions

### **Timeline Risks**
1. **P0 Overruns**: If P0 takes >3 weeks, delay P1 or descope P2
2. **Diagram Complexity**: Mermaid diagrams can be time-intensive
   - **Mitigation**: Use simple flowcharts/sequence diagrams, not class diagrams

---

## I. Next Steps

### **Immediate Actions (This Week)**
1. ✅ Review and approve this research plan
2. 🔲 Create work items for P0 tasks (P0-1 through P0-4)
3. 🔲 Assign research tasks to team members (if multi-person) or self
4. 🔲 Set up code sample templates in `samples/` directories

### **Week 1 Kickoff**
1. Research T1486, T1485, T1499 defenses (Impact tactics)
2. Outline Reconnaissance defense patterns (T1592, T1595)
3. Draft C2 detection code (T1071, T1572)
4. Begin Mermaid diagram sketches

---

## J. Open Questions

1. **Language Prioritization**: Should P2 add Go first or Rust first? (Recommend Go — more common in cloud-native)
2. **Mobile Content**: Is mobile app security in scope, or web/API-only? (Recommend defer to P2 or separate deck)
3. **Live Demos**: Should we create runnable Docker Compose environments for demos? (Recommend yes, separate repo)
4. **ATT&CK Version**: Track ATT&CK v16 (current) or wait for v17? (Recommend v16, update later)

---

## K. Appendix: ATT&CK Tactic Reference

| Tactic ID | Tactic Name | Current Coverage | Priority |
|-----------|-------------|------------------|----------|
| TA0043 | Reconnaissance | ❌ Missing | P0 |
| TA0042 | Resource Development | ❌ Missing | P0 |
| TA0001 | Initial Access | ✅ Full | Maintain |
| TA0002 | Execution | ✅ Full | Maintain |
| TA0003 | Persistence | ✅ Full | Maintain |
| TA0004 | Privilege Escalation | ✅ Full | Maintain |
| TA0005 | Defense Evasion | ✅ Full | Maintain |
| TA0006 | Credential Access | ✅ Full | Maintain |
| TA0007 | Discovery | ✅ Full | Maintain |
| TA0008 | Lateral Movement | ✅ Full | Maintain |
| TA0009 | Collection | 🟡 Partial | P0 |
| TA0011 | Command & Control | ❌ Missing | P0 |
| TA0010 | Exfiltration | 🟡 Partial (in Collection) | P0 |
| TA0040 | Impact | 🟡 Partial | P0 |

**Total**: 14 tactics, 8 full, 3 partial, 3 missing

---

**End of Research Plan**

**Approval Required From**: Chris Ayers  
**Next Review Date**: After P0 completion (Week 3)
