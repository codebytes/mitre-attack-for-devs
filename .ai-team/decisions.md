# Decisions

> Team decisions that all agents must respect. Maintained by Scribe.

---

# Decision: ATT&CK Research Document Complete

**Date:** 2025-02-21  
**Author:** Fenster  
**Status:** Complete

## Summary

Created comprehensive ATT&CK research document at `.ai-team/agents/fenster/attack-research.md` to serve as the authoritative reference for developers building ATT&CK-aware applications.

## Document Structure

### 1. The 14 ATT&CK Tactics — Developer Relevance
- All 14 tactics (TA0043 through TA0040)
- Each includes: tactic ID, description, why developers should care (2-3 sentences), and top 3 relevant techniques with defenses
- Focus on application-layer concerns and developer-controllable mitigations

### 2. Developer-Centric Technique Deep Dives
- 15 high-priority techniques analyzed in depth: T1190, T1059, T1078, T1195, T1552, T1070, T1110, T1567, T1499, T1565, T1098, T1134, T1505.003, T1021, T1213
- Each technique includes 4-5 sentences covering: what it is, how attackers use it, how developers defend
- Emphasizes practical, code-level defenses

### 3. OWASP Top 10 2025 → ATT&CK Mapping
- Complete table mapping all 10 OWASP categories to relevant ATT&CK techniques
- Bridges vulnerability-focused (OWASP) and adversary-focused (ATT&CK) perspectives
- Enables developers to understand attack techniques through familiar OWASP lens

### 4. Modern Attack Chains
- 5 realistic multi-stage attack scenarios demonstrating technique chaining
- Scenarios: Supply Chain to Persistence, Initial Access to Data Breach, Credential Stuffing to Lateral Movement, File Upload to Web Shell, API Abuse to Mass Exfiltration
- Each chain shows 7-8 sequential techniques with T-codes

### 5. MITRE D3FEND Mappings
- 20 defensive techniques mapped to D3FEND IDs
- Links defensive patterns to techniques they mitigate
- Provides standardized vocabulary for defensive measures

### 6. Emerging Techniques (2024-2026)
- 5 emerging attack areas: AI/ML Security, Cloud-Native Attacks, API-Specific Attacks, Container/Orchestration Risks, CI/CD Pipeline Targeting
- Each area analyzed for 2-3 sentences with ATT&CK technique analogies
- Future-focused content for modern development practices

## Key Design Decisions

1. **Developer-first language**: Avoided security jargon, used practical code examples and familiar vulnerability types (IDOR, ReDoS, etc.)
2. **Actionable defenses**: Every technique includes concrete defensive measures developers can implement
3. **OWASP bridge**: Mapped ATT&CK to OWASP Top 10 2025 to leverage existing developer knowledge
4. **Technique prioritization**: Focused on application-layer techniques developers can actually mitigate in code
5. **Modern context**: Emphasized microservices, cloud, containers, and CI/CD—reflecting current development practices

## Coverage Analysis

- **Complete**: All 14 tactics covered
- **Deep dives**: 15 priority techniques analyzed
- **Mappings**: OWASP, D3FEND, attack chains provided
- **Forward-looking**: Emerging techniques section for 2024-2026 threats

## Usage

This document serves as:
- Reference for slide content development (McManus)
- Source material for code examples (Hockney)
- Threat modeling input (all team members)
- Training material foundation for developer security education

## Next Steps

- McManus can extract key points for slides
- Hockney can reference defensive patterns for code examples
- Keaton can use attack chains for test scenario development
- Document should be updated quarterly as ATT&CK framework evolves

---

# Keaton's Accuracy Audit - Key Findings & Decisions

**Audit Date:** 2026-02-22  
**Auditor:** Keaton (Tester/QA)  
**Status:** READY FOR REVIEW

---

## Executive Summary

**Overall Assessment: A- (Excellent with 2 critical clarifications needed)**

The MITRE ATT&CK content is highly accurate. All 40+ technique IDs are correct, code samples properly demonstrate vulnerabilities and defenses, and content is consistent across all materials. **No errors found, only clarifications needed.**

---

## Critical Issues Requiring Immediate Action

### 1️⃣ OWASP-to-ATT&CK Mapping Needs Clarification
**Priority:** CRITICAL (affects instructor teaching)  
**Location:** Slides.md - "OWASP & MITRE ATT&CK Comparison" table

**Current Problem:**
```
Broken Access Control | T1078 (Valid Accounts), T1098, T1068
Injection            | T1190, T1059
```

**Why This Matters:**
- Students conflate **vulnerabilities** (OWASP) with **techniques** (ATT&CK)
- T1078 is not a "broken access control vulnerability"—it's using compromised legitimate creds
- T1059 (Command Execution) is NOT an injection vulnerability; injection can *lead to* T1059

**Recommended Fix:**
Add clarifying sentence in slides before table:
> "**Important:** OWASP describes vulnerabilities; ATT&CK describes attack techniques. Vulnerabilities can enable techniques, but they're distinct concepts. For example, command injection vulnerabilities can enable T1059 execution."

Then reorder table to clarify the relationship.

**Acceptance Criteria:**
- [ ] Slides explicitly define the OWASP vs ATT&CK distinction
- [ ] Table mapping is reviewed by content owner
- [ ] One teaching example shows OWASP vulnerability → ATT&CK technique chain

---

### 2️⃣ Confirm T1059.006 vs T1203 Classification
**Priority:** CRITICAL (for grading accuracy)  
**Location:** `unsafe_deserialization.py` - Python sample docstring

**Current State:**
- Code is labeled T1059.006 (Python-specific)
- Could also be T1203 (Exploitation for Client Execution - broader)

**Audit Result:** ✅ **VERIFIED CORRECT**
- T1059.006 is the correct classification for Python pickle deserialization
- T1203 would apply to Java/other binary deserialization
- No change needed ✓

**Recommendation:** Document this for instructors:
> Add comment: "Python's pickle vulnerability is T1059.006 (Python-specific). Other language deserialization exploits may map to T1203 (general client execution)."

---

## Coverage Gaps (Informational)

### Not Blocking, But Should Document Scope

#### Gap #1: T1078 (Valid Accounts) - No Code Sample
- **Mentioned:** Slides only
- **Missing:** Authentication anomaly detection code
- **Impact:** Students see login monitoring examples but no automated detection sample
- **Recommendation:** Add note in README: "T1078 detection covered implicitly in login examples; dedicated authentication monitoring sample would enhance coverage"

#### Gap #2: T1110 vs T1110.004
- **Current:** Only credential stuffing (T1110.004) has samples
- **Missing:** Password spraying detection (T1110)
- **Impact:** Minor - both are attack variations; current sample is most practical
- **Recommendation:** In README, clarify: "Samples focus on credential stuffing (T1110.004). Parent technique T1110 includes password spraying, dictionary attacks."

#### Gap #3: T1565 (Data Manipulation) - No Code Sample
- **Mentioned:** Slides only - data integrity section
- **Missing:** Implementation of integrity verification
- **Impact:** Integrity protection is theoretical only
- **Recommendation:** Add sample or note "Integrity patterns implemented in logging samples (TamperEvidentLogger)"

---

## Verified Accurate (No Issues)

### ✅ All Technique IDs Correct (40 techniques)
Every technique ID referenced has been verified against official MITRE ATT&CK. No deprecated IDs, no incorrect mappings.

### ✅ Code Sample Quality (12/12 reviewed)
- Vulnerable code is actually exploitable
- Defended code actually mitigates
- All defensive patterns are correct
- Multi-language implementations are consistent

### ✅ Documentation Consistency
- READMEs match actual files
- Slides match code samples
- Descriptions accurate

### ✅ Defensive Techniques Sound
- Input validation patterns: Correct allowlists, no blacklists
- Output encoding: Proper sanitization
- Authentication: Modern practices (MFA concepts, token validation)
- Logging: Tamper-evident hash chains are cryptographically sound

---

## Action Items for Team

### For Chris (Content Owner)
- [ ] Review OWASP vs ATT&CK clarification and approve wording
- [ ] Decide if additional samples needed for T1078, T1110, T1565
- [ ] Document T1059.006 vs T1203 distinction for instructors

### For Keaton (QA - Follow-up)
- [ ] Verify slides are updated with OWASP/ATT&CK clarification
- [ ] Confirm any new samples added maintain accuracy standards
- [ ] Review updated materials for consistency

### For Developer (if adding samples)
- [ ] Any new samples should follow existing pattern:
   - Vulnerable code first (clearly marked ❌)
   - Defended code second (clearly marked ✅)
   - Comments linking to technique ID (e.g., `# T1078 Defense: ...`)
   - Realistic scenario, not contrived example

---

## Audit Completeness Checklist

- [x] All files in slides/Slides.md reviewed
- [x] All Python samples analyzed for accuracy
- [x] All .NET samples analyzed for accuracy
- [x] All JavaScript samples spot-checked for accuracy
- [x] All README files verified for consistency
- [x] All technique IDs verified against official framework
- [x] Coverage matrix created
- [x] Code samples tested for logical soundness
- [x] Defensive patterns validated

**Audit Status:** ✅ COMPLETE

---

## Final Recommendation

**Status: APPROVED WITH MINOR REVISIONS**

This content is accurate and ready for use. Implement the OWASP/ATT&CK clarification before final release. Consider adding coverage notes for documentation completeness.

**Grade: A- (Excellent)**

---

**Signed:** Keaton  
**Date:** 2026-02-22  
**Confidence Level:** HIGH - All claims verified through code review and framework cross-reference

---

### 2026-02-22: MITRE ATT&CK Research Architecture — 3-Phase Expansion Plan

**By:** Kobayashi  
**Status:** Proposed

**What:** Structured research plan to expand MITRE ATT&CK for Developers content from 11 to 14 fully-covered tactics, add 5 realistic attack chain scenarios, and increase code samples from 17 to 35+.

**Why:** 
- Current slides have strong individual technique coverage but 3 critical gaps: Reconnaissance, Command & Control, and Resource Development tactics are missing or superficial
- Impact section ends abruptly (line 1194) with no ransomware/data destruction defenses
- No cross-tactic attack chains — real adversaries chain techniques, our content treats them in isolation
- This limits practical value for threat modeling and incident response training

**How:**
- **P0 (Weeks 1-3)**: Close critical gaps — complete Reconnaissance, C2, Impact, Collection sections. +20 slides, +8 code samples, +4 diagrams.
- **P1 (Weeks 4-7)**: Build 5 attack chain scenarios (Web Takeover, Credential Compromise, Supply Chain, Session Hijacking, Ransomware). +20 slides, +10 code samples, +6 diagrams.
- **P2 (Weeks 8-12, Optional)**: Add Go/Rust samples, mobile security, CI/CD hardening content. +15 slides, +15 samples.

**Impact:**
- Complete 14/14 ATT&CK tactic coverage (currently 8 full, 3 partial, 3 missing)
- 50+ techniques with code examples (currently ~30)
- All P0/P1 techniques have examples in 2+ languages
- Final slide deck: ~2200 lines (from 1531), 35+ code samples (from 17)

**Risks & Mitigations:**
- Scope creep: Cap attack chains at 5 scenarios, 200 total slides
- Code complexity: Use simulation code, not actual exploits
- Maintenance burden: Focus on patterns, not library-specific code

**Next Steps:**
1. Review/approve plan
2. Create P0 work items (P0-1: Impact completion, P0-2: Reconnaissance, P0-3: C2, P0-4: Collection/Exfil)
3. Begin Week 1 research: T1486, T1485, T1499 defenses

**Full Plan:** `.ai-team/decisions/inbox/kobayashi-research-plan.md`

---

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

---

# Slide Expansion Strategy: MITRE ATT&CK for Developers

**Decision Date**: 2026-02-22  
**Decided By**: McManus (Content Dev)  
**Status**: 🔴 BLOCKING (Speaker Notes) → 🟡 ACTIVE (Expansion Planning)  

---

## Decision 1: Speaker Notes are Mandatory

**Context**: The slide deck exists with 71 slides covering 10 ATT&CK tactics, but has **zero speaker notes**.

**Decision**: 
> All slides must have speaker notes before the deck is presented live.

**Rationale**:
- A deep-dive presentation requires context, examples, and Q&A talking points
- Without speaker notes, Chris will need to memorize or improvise, reducing delivery confidence
- Speaker notes serve dual purpose: delivery aide + future reference for other presenters
- Expected delivery time is 45–75 minutes; notes help with pacing

**Implementation**:
- Add `<!-- SPEAKER NOTES: ... -->` HTML comment block to each slide
- For technical slides: explain the "why," real-world examples, common questions
- For overview slides: clarify key messages and transition language
- Format: consistent template for all slides (see slide-analysis.md section E)

**Owner**: McManus  
**Timeline**: Must complete before first live presentation  

---

## Decision 2: Complete All 14 ATT&CK Tactics

**Context**: Current deck covers 10/14 tactics:
- ✅ Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection/Exfiltration, Impact
- ❌ Reconnaissance, Resource Development, Command & Control (partially covered in 1/2 slide)

**Decision**: 
> Expand the deck to comprehensively cover all 14 tactics with 2–5 slides each.

**Rationale**:
- For a "deep dive research project," incomplete coverage is misleading

---

# Decision: Speaker Note Conventions for Marp Presentations

**Date:** 2026-02-22  
**Author:** McManus (Content Dev)  
**Status:** Established

## Summary

Speaker notes for Marp slide decks use HTML comment syntax and follow specific content and placement conventions.

## Context

The MITRE ATT&CK for Developers presentation deck lacked speaker notes, making it difficult for presenters to deliver consistently or for other speakers to pick up the deck. For a 60-75 minute technical deep-dive, comprehensive speaker notes are essential for pacing, transitions, and audience engagement.

## Conventions Established

### Placement
- Speaker notes go **after slide content** but **before the `---` separator**
- Format: `<!-- Speaker notes content here -->`
- Multi-line notes are supported and preferred

### Content Guidelines
- **Length**: 2-5 sentences per slide
- **Coverage**: 
  - Key talking points for the presenter
  - Transition cues ("This leads us to...", "Building on that...")
  - Real-world anecdotes or examples to mention
  - Timing guidance for important slides ("Spend 2-3 minutes here")
  - Audience engagement prompts ("Ask the audience...", "Show of hands...")

### Slide-Type Specific Guidance
- **Code slides**: Explain what to highlight, what to walk through line by line
- **Diagram slides**: Describe the flow to narrate
- **Section header slides**: Set up what's coming next
- **Intro/bio slides**: Mention audience warm-up points
- **Closing slides**: Wrap-up talking points and calls to action
- **Concept slides**: Provide analogies and context

### Style
- Write in presenter's voice (direct, conversational)
- Include explicit timing and emphasis cues
- Provide context that helps presenters who know security but may not have memorized every ATT&CK technique
- Balance technical depth with accessibility

## Rationale

1. **Consistency**: Enables multiple presenters to deliver the same content with consistent messaging
2. **Pacing**: Helps manage a 60-75 minute presentation across 71+ slides
3. **Engagement**: Prompts for audience interaction prevent monotony
4. **Transitions**: Explicit cues create smooth flow between sections
5. **Confidence**: Detailed notes give presenters confidence to deliver complex technical material

## Examples

### Good Example (Code Slide)
```markdown
## Vulnerable Code: SQL Injection (T1190)

[code block]

<!-- 
Classic SQL injection vulnerability. We're taking user input and directly concatenating it into a SQL query—no validation, no parameterization. The attack payload at the bottom shows how an attacker sends "1 OR 1=1--" to dump the entire users table. This enables T1190: Exploit Public-Facing Application. We've all seen this in training, but it's still the number one web app vulnerability in the wild. Let's see the fix.
-->
```

### Good Example (Section Header)
```markdown
# <!-- fit --> Initial Access & Credential Attacks

<!-- 
First tactic: Initial Access. How do attackers get in? Through your front door—public-facing applications, stolen credentials, brute force attacks, and phishing. This is the most critical phase to defend because stopping them here prevents everything downstream. Let's look at the techniques.
-->
```

## Team Impact

- Presentations can be delivered by multiple team members with consistent quality
- New speakers can onboard to the deck quickly
- Conference organizers receive presentation-ready material
- Speaker notes serve as mini-documentation of security concepts

## Related Decisions

- See `.ai-team/agents/mcmanus/history.md` for full slide deck analysis
- Marp conventions documented in project custom instructions

---

# Decision: MITRE ATT&CK for Developers — BUILD ORDER

**Author:** Kobayashi (Lead / Architect)  
**Date:** 2026-02-22  
**Status:** READY FOR TEAM EXECUTION  

## Overview

Based on **Fenster's attack research**, **Keaton's accuracy audit**, and **McManus's slide analysis**, this document prioritizes the work into **7 sequential builds** that unblock downstream work and maximize impact per effort.

**Key Principle:** Fix critical clarity issues first, then close coverage gaps, then expand to full tactic coverage.

## BUILD PRIORITY MATRIX

| # | Task | Who | Effort | Blocker? | Dependency | Timeline |
|---|------|-----|--------|----------|------------|----------|
| **1** | Fix OWASP-ATT&CK mapping clarity in slides | McManus | 1h | YES | None | Day 1 |
| **2** | Add speaker notes to all 71 slides | McManus | 6h | YES | Task #1 | Day 1–2 |
| **3** | Add 3 critical code samples (T1078, T1110, T1565) | Fenster | 4h | NO | Task #2 | Day 2 |
| **4** | Expand Reconnaissance tactic (1→3 slides + code) | McManus | 3h | NO | Task #1 | Day 2 |
| **5** | Expand Resource Development tactic (1→2 slides + code) | McManus | 2h | NO | Task #1 | Day 2 |
| **6** | Expand Command & Control tactic (1→2 slides + code) | Fenster | 2h | NO | Task #3 | Day 3 |
| **7** | Add recap slides + speaker validation + final export | McManus | 3h | NO | All above | Day 3 |

**Total Team Effort:** 21 hours  
**Estimated Timeline:** 3 days (parallel work possible)  
**Success Metrics:** 14/14 tactics covered, 100% speaker notes, Keaton audit grade: A

## TASK DETAILS

### **TASK #1: Fix OWASP-ATT&CK Mapping Clarity** 
**Owner:** McManus (Content Dev)  
**Effort:** 1 hour  
**Why First:** Critical clarity issue (Keaton Issue #2). Blocks speaker notes.

**What to do:**
1. Open `slides/Slides.md`, find "OWASP & MITRE ATT&CK Comparison" section (~line 150–200)
2. Add introductory paragraph before the mapping table:
   ```markdown
   > **Key Distinction:** OWASP Top 10 describes *vulnerabilities* (what can break). 
   > MITRE ATT&CK describes *techniques* (how attackers operate). A single vulnerability 
   > can enable multiple techniques. For example, SQL injection (OWASP A03) can lead to 
   > T1190 (Exploit Public-Facing Application) OR T1213 (Data Collection) depending on 
   > attacker intent.
   ```
3. Revise mapping table entries:
   - Move T1078 from "Broken Access Control" → "Identification & Authentication Failures" (correct tactic relationship)
   - Add footnote to T1059: "Command injection (OWASP A03) can *enable* T1059 execution"
4. Validate against Fenster's mapping section (decisions.md line reference to be added)

**Inputs:** Keaton audit, Fenster mapping (decisions.md)  
**Output:** Updated `slides/Slides.md` with clarified mapping  
**Validation:** Keaton re-review of mapping section

---

### **TASK #2: Add Speaker Notes to All 71 Slides**
**Owner:** McManus (Content Dev)  
**Effort:** 6 hours  
**Why:** Blocking item for live delivery. Keaton/McManus both flagged absence.

**What to do:**
1. For each slide, add `<!-- SPEAKER NOTES: ... -->` HTML comment block covering:
   - **What (What's the technique/concept?)**
   - **Why (Why should developers care? Business + technical impact)**
   - **Real-world example (Actual breach, CVE, or incident)**
   - **Audience Q&A Talking Points (3–5 common questions + concise answers)**
   - **Delivery Notes (Pacing, emphasis, pause points)**

2. **Priority order** (do these first, then the rest):
   - Initial Access slides (T1190, T1078, T1110)
   - Execution slides (T1059, T1203)
   - Persistence slides (T1185, T1505.003)
   - Privilege Escalation slides (T1068, T1134)
   - **Then**: Credential Access, Defense Evasion, Discovery, Supply Chain, Lateral Movement, Collection/Exfil, Impact, Closing

3. **Template for each slide:**
   ```markdown
   <!-- 
   SPEAKER NOTES: [Technique Name]
   
   What:
   - [Technique definition in 1–2 sentences]
   
   Why:
   - Developer impact: [what can break]
   - Business impact: [what attackers gain]
   
   Real-World Example:
   - [Actual incident: Year, Company, Technique ID]
   - Link: [CVE or reference]
   
   Audience Q&A:
   - Q: "How do I know if I'm vulnerable?"
     A: [Practical detection steps]
   - Q: "What's the fastest fix?"
     A: [Quick win + comprehensive solution]
   
   Delivery:
   - Time: 2 min (for code-heavy), 1 min (for overview)
   - Pause after: [key vulnerability shown]
   - Emphasize: [most important defense]
   -->
   ```

**Inputs:** McManus analysis, Fenster attack research (for real-world examples)  
**Output:** `slides/Slides.md` with 71 speaker note blocks  
**Validation:** Chris reviews for tone, timing; delivery test on 3 slides

---

### **TASK #3: Add 3 Critical Code Samples (Coverage Gaps)**
**Owner:** Fenster (Security Researcher)  
**Effort:** 4 hours  
**Why:** Closes Keaton's 3 major coverage gaps. Enable Task #4–7.

**What to do:** Create 3 new code samples + corresponding README entries:

#### **3a. Authentication Monitoring (T1078 - Valid Accounts)**
**File:** `samples/python/authentication_monitoring.py`

**Content:**
- Baseline authentication behavior tracking (login time, location, device fingerprint)
- Anomalous login detection (unusual geolocation, device change, off-hours)
- Automatic session invalidation on suspicious activity
- Real-world: Use geolocation API + device fingerprinting library

**Vulnerable scenario:** No monitoring → attackers use compromised account indefinitely  
**Defended scenario:** Baseline + alerts → detect T1078 within minutes

**Sample lines:** 100–150 lines  
**Input source:** Fenster's T1078 section in attack-research.md (lines 169–174)

---

#### **3b. Credential Stuffing Detection Enhanced (T1110 Broader Scope)**
**File:** `samples/python/password_spray_detection.py`

**Content:**
- Expand beyond credential stuffing to password spraying (many accounts, few passwords)
- Dictionary attack detection (common password patterns)
- Distributed brute force detection (rate-limiting per IP + account)
- Velocity-based triggers (attempts per minute across accounts)

**Vulnerable scenario:** Standard rate limiting on login endpoint → attackers spray from botnets  
**Defended scenario:** Distributed attack detection + CAPTCHA + account lockout → T1110 blocked

**Sample lines:** 120–150 lines  
**Input source:** Fenster's T1110 section (lines 197–202)

---

#### **3c. Data Integrity Verification (T1565 - Data Manipulation)**
**File:** `samples/javascript/data_integrity_verification.js`

**Content:**
- HMAC-based integrity verification for sensitive database records
- Soft delete with audit trail (for T1485 - Data Destruction)
- Change detection: compare record hash before/after modification
- Alerting on unexpected data changes
- Real-world: E-commerce order amounts, user privilege fields, configuration values

**Vulnerable scenario:** No integrity checks → attackers modify order amounts undetected  
**Defended scenario:** HMAC verification → detect modification immediately

**Sample lines:** 150–180 lines  
**Input source:** Fenster's T1565 section (lines 218–223)

---

**Deliverables:**
- 3 new files in `samples/{python,javascript}/`
- Updated `samples/python/README.md` + `samples/javascript/README.md` with 3 new entries
- Each sample includes:
  - Vulnerable code (what attackers exploit)
  - Defended code (detection + mitigation)
  - Detailed comments linking to T-code + OWASP
  - Real-world scenario description

**Validation:** Keaton re-tests code samples. All 3 achieve "ACCURATE" rating.

---

### **TASK #4: Expand Reconnaissance Tactic (1→3 Slides + Code)**
**Owner:** McManus (Content Dev)  
**Effort:** 3 hours  
**Why:** Close Keaton/McManus gap on Reconnaissance. Expands deck from 71→74 slides.

**What to do:** Add 3 new slides after current Slide 57 (Reconnaissance/C2/Resource Dev brief):

#### **Slide X1: Reconnaissance Techniques Overview**
Content:
- Table of 3 key techniques: T1592 (Gather Victim Host Info), T1595 (Active Scanning), T1589 (Gather Victim Identity Info)
- Developer role: Reduce information leakage through error messages, API responses, metadata

**Slide X2: Vulnerable Code — Verbose Error Messages (T1592)**
Content:
```
# VULNERABLE - Stack trace leaks framework version, OS details
except Exception as e:
    return {"error": str(e), "traceback": traceback.format_exc()}
```

**Slide X3: Defended Code — Generic Errors**
Content:
```
# DEFENDED - Generic response, internal logging
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return {"error": "Internal server error", "code": "ERR_500"}
```

**Input source:** Fenster's TA0043 section (lines 11–19)

---

### **TASK #5: Expand Resource Development Tactic (1→2 Slides + Code)**
**Owner:** McManus (Content Dev)  
**Effort:** 2 hours  
**Why:** Close gap on Resource Development. Adds 2 slides (71→73).

**What to do:** Add 2 new slides:

#### **Slide Y1: Resource Development Techniques Overview**
Content:
- T1583 (Acquire Infrastructure), T1587 (Develop Capabilities), T1608 (Stage Capabilities)
- Developer role: Detect when your services are being weaponized (compromised accounts, API abuse)

#### **Slide Y2: Code Example — Webhook Signature Verification (T1587/T1608)**
Content:
```
# VULNERABLE - Accept webhook without verifying sender
@app.post("/webhook")
def webhook_receiver(payload):
    execute_action(payload)  # Could be malicious

# DEFENDED - Verify HMAC-SHA256 signature
import hmac, hashlib

def verify_webhook(payload, signature):
    expected = hmac.new(SECRET_KEY, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

@app.post("/webhook")
def webhook_receiver(payload, signature):
    if not verify_webhook(payload, signature):
        return {"error": "Invalid signature"}, 403
    execute_action(payload)
```

**Input source:** Fenster's TA0042 section (lines 21–29)

---

### **TASK #6: Expand Command & Control Tactic (1→2 Slides + Code)**
**Owner:** Fenster (Security Researcher)  
**Effort:** 2 hours  
**Why:** Close gap on C2. Adds 2 slides (71→73).

**What to do:** Add 2 new slides:

#### **Slide Z1: Command & Control Techniques Overview**
Content:
- T1071 (Application Layer Protocol), T1572 (Protocol Tunneling), T1573 (Encrypted Channel)
- Developer role: Detect C2 communications hidden in normal traffic (beaconing, unusual patterns)
- Diagram: Network traffic analysis workflow (Mermaid)

#### **Slide Z2: Code Example — Detecting C2 Beaconing (T1071)**
Content:
```
# Detect C2 beaconing: regular API calls to external endpoint
# DETECTION CODE:
def detect_c2_beaconing(api_logs, threshold_interval=300):
    """Alert if outbound API calls are suspiciously regular"""
    intervals = []
    for i in range(1, len(api_logs)):
        delta = api_logs[i].timestamp - api_logs[i-1].timestamp
        intervals.append(delta)
    
    # Check if intervals are suspiciously consistent (±10 sec)
    avg_interval = sum(intervals) / len(intervals)
    variance = sum((x - avg_interval)**2 for x in intervals) / len(intervals)
    
    if variance < 100 and avg_interval == threshold_interval:
        return {"alert": "C2_BEACONING", "interval": avg_interval}
```

**Input source:** Fenster's TA0011 section (lines 121–129)

---

### **TASK #7: Add Recap Slides + Final Validation**
**Owner:** McManus (Content Dev)  
**Effort:** 3 hours  
**Why:** Narrative closure. Ties everything together. Final validation before presentation.

**What to do:**

#### **New Slide: "Technique Coverage Map"**
Content:
- Mermaid heatmap showing:
  - Which tactics have code examples (GREEN)
  - Which have diagrams (BLUE)
  - Which are high-priority for developers (RED)
- Emphasize: 14/14 tactics now covered

#### **New Slide: "What We Didn't Cover (But You Should Know)"**
Content:
- Brief table of 4 tactics less developer-relevant (e.g., Resource Development mostly attacker-controlled)
- Pointer to MITRE docs for deeper study

#### **New Slide: "Your Next Steps" (Call-to-Action)**
Content:
- Week 1: Pick one technique + implement monitoring
- Week 2: Threat model your top 3 services using ATT&CK
- Week 3+: Run through defense checklist (from slides/checklists/)
- Ongoing: Subscribe to MITRE updates, ATT&CK Navigator

#### **Final Steps:**
1. **Validate Marp rendering:** Export to HTML + PDF
2. **Verify all images load:** `portrait.png`, `owl.png`
3. **Check Mermaid rendering:** All 10+ diagrams render correctly
4. **Test speaker notes:** Open in Marp presenter view, test timing
5. **Get Chris signoff:** Review final deck for tone, messaging, pacing

**Deliverables:**
- 3 new recap/closure slides
- `slides/Slides.md` updated with full content
- `slides/Slides.pdf` export (test artifact)
- Updated `.ai-team/agents/kobayashi/history.md` with learnings

---

## EXECUTION ROADMAP

### **Day 1 (Parallel Possible)**
- ✅ **Morning:** McManus completes Task #1 (OWASP mapping clarity fix)
- ✅ **Morning:** Fenster preps code sample stubs for Task #3
- ✅ **Afternoon:** McManus begins Task #2 (speaker notes — Phase 1: Initial Access + Execution)

### **Day 2 (Parallel)**
- ✅ **Morning:** McManus continues Task #2 (Phase 2: Persistence + Privilege Escalation)
- ✅ **Morning:** Fenster implements Task #3 code samples (3 files + READMEs)
- ✅ **Afternoon:** McManus completes Task #2
- ✅ **Afternoon:** McManus starts Task #4 (Reconnaissance expansion)

### **Day 3 (Parallel → Sequential)**
- ✅ **Morning:** McManus completes Task #4 + Task #5 (Recon + Resource Dev)
- ✅ **Morning:** Fenster completes Task #6 (C2 expansion)
- ✅ **Afternoon:** McManus starts Task #7 (recap slides + validation)
- ✅ **Afternoon:** Keaton spot-checks samples (Task #3)
- ✅ **EOD:** Chris reviews final deck

### **Signoff**
- [ ] Keaton: Code sample audit (Task #3) → Grade: A
- [ ] McManus: Speaker notes quality check → Complete
- [ ] Chris: Deck review + approval → Ready for presentation

---

## INPUTS & ARTIFACTS

**Available Inputs:**
- `slides/Slides.md` (current 71 slides, 1530 lines)
- `.ai-team/agents/fenster/attack-research.md` (44KB reference)
- `.ai-team/agents/keaton/accuracy-audit.md` (7 findings + recommendations)
- `.ai-team/agents/mcmanus/slide-analysis.md` (gap analysis)
- `samples/{python,dotnet,javascript}/` (existing code structure)

**Outputs:**
- Updated `slides/Slides.md` (~2200 lines, 80–85 slides, full coverage)
- 3 new code samples (authentication, password spray, data integrity)
- Updated README files
- 100% speaker notes coverage
- PDF export for distribution
- Updated `.ai-team/agents/kobayashi/history.md` with lessons learned

---

## SUCCESS CRITERIA

| Criterion | Owner | Target | Validation |
|-----------|-------|--------|------------|
| OWASP-ATT&CK mapping clarified | McManus | Zero ambiguity on vulnerability vs. technique | Keaton re-review |
| Speaker notes complete | McManus | 100% of slides (71+) have notes | Delivery test (3 slides) |
| 3 critical samples added | Fenster | T1078, T1110, T1565 all have working code | Keaton audit = "ACCURATE" |
| Reconnaissance fully covered | McManus | 3 slides + code = A-level coverage | Keaton matrix update |
| Resource Dev fully covered | McManus | 2 slides + code = B-level coverage | Keaton matrix update |
| C2 fully covered | Fenster | 2 slides + detection code | Keaton matrix update |
| 14/14 tactics covered | McManus | No tactic gaps remain | Final audit |
| Final validation | McManus | Marp → PDF export passes all checks | PDF renders cleanly |

---

## RISK MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Speaker notes take >6 hours | Medium | Blocks Task #2 completion | Break into 2 parallel phases |
| Code samples have bugs | Low | Keaton audit fails | Fenster tests locally before commit |
| Slide deck exceeds 85 slides | Low | Delivery > 75 min | Condense less impactful sections |
| Marp export fails (image paths) | Low | PDF unrenderable | Test on Day 1; use relative paths |
| Chris requests major rewrites | Medium | Timeline slip | Lock slide content by EOD Day 2 |

---

## DECISION CHECKPOINTS

**BEFORE TASK #2:** Confirm OWASP mapping is correct (McManus + Keaton sign-off)  
**BEFORE TASK #4:** Confirm Task #3 code samples pass audit (Keaton sign-off)  
**BEFORE TASK #7:** Confirm all 6 prior tasks complete (Kobayashi checkpoint)  
**FINAL SIGNOFF:** Chris approves deck + speaker notes for live delivery

---

## NOTES FOR THE TEAM

1. **McManus** is the critical path. Ensure she has uninterrupted time for speaker notes (Task #2). This is the most time-consuming work.
2. **Fenster's code samples** (Task #3) should follow Keaton's audit pattern: vulnerable code first, then defended code, with clear comments.
3. **Slides should expand to 80–85 total** (from current 71). Each tactic gets 3–5 slides minimum. This is already planned in the architecture.
4. **Speaker notes are non-negotiable.** Chris will need these for confident delivery. Include real-world examples, not just framework definitions.
5. **Keaton's audit findings** are steering this work. Trust her classification of severity. The OWASP-ATT&CK mapping (Issue #2) is critical and must be fixed first.

---

## SUCCESS VISION

After this 3-day sprint:
- ✅ Slides: 85 slides covering 14/14 tactics, 100% speaker notes, professional Marp export
- ✅ Code: 3 new samples (T1078, T1110, T1565) validated by Keaton
- ✅ Clarity: OWASP vs. ATT&CK distinction crystal clear; no student confusion
- ✅ Delivery: Chris can present confidently with full speaker notes and real-world examples
- ✅ Grade: Keaton upgrades audit from A- → **A**

This becomes a **reference-grade deep-dive resource** that Chris can reuse for multiple audiences and the team can maintain/extend over time.

---

**Document Owner:** Kobayashi  
**Status:** READY FOR TEAM EXECUTION  
**Next Step:** Chris confirms team availability + starts Day 1
- Missing tactics leave audience with gaps when implementing defenses
- Reconnaissance and Resource Development, while "less developer-focused," are critical for threat modeling
- Creates a reusable reference for all 14 tactics

**Specific Actions**:
1. **Reconnaissance (TA0043)**: Add 3 slides
   - Technique overview (T1592, T1595, T1598)
   - Code: Verbose error messages + defense
   - Guidance: Hardening API metadata, error handling

2. **Resource Development (TA0042)**: Add 2 slides
   - Technique overview (T1583, T1584, T1600)
   - Code: Webhook validation, OAuth audit

3. **Command & Control (TA0011)**: Add 2 slides
   - Technique overview (T1071, T1572)
   - Code: Detecting C2 over HTTPS, TLS pinning

4. **Review Lateral Movement**: Currently 3 slides; improve clarity
   - Separate Python and JavaScript code examples
   - Add detection monitoring slide

**Owner**: McManus  
**Timeline**: Weeks 1–2 of expansion phase  
**Output**: 5–7 new slides, 10–12 updated slides

---

## Decision 3: Narrative Closure Required

**Context**: The deck ends abruptly at slide 71 (Questions?) with no recap of covered techniques, no clear "next steps" for the audience, and no acknowledgment of missing tactics.

**Decision**: 
> Add 3–4 closure slides before the final "Questions?" slide.

**Rationale**:
- Audiences retain information better with explicit recap
- "Next steps" turn knowledge into action (critical for adoption)
- Transparency about scope (what we covered vs. what we didn't) builds credibility

**Specific Slides to Add**:
1. **Technique Coverage Matrix** (new)
   - Mermaid heatmap or table showing which tactics have code examples, diagrams, detection patterns
   - Color-code by developer responsibility (HIGH, MEDIUM, LOW)
   - Audience insight: "Here's what you're responsible for"

2. **What We Didn't Cover** (new)
   - Table: 4 missing/partial tactics + brief description + pointer to MITRE docs
   - Messaging: "These are important; here's where to research further"

3. **Your 90-Day Roadmap** (enhance existing "Start Small" slide)
   - Week 1–2: Pick one technique (T1078 recommended)
   - Week 3–4: Implement detection logging with ATT&CK ID tagging
   - Month 2: Expand to 3 techniques
   - Month 3: Integrate with security workflows
   - Call-to-action: "Commit to one technique this week"

**Owner**: McManus  
**Timeline**: Week 2 of expansion phase  
**Output**: 3–4 new slides, 1 enhanced slide

---

## Decision 4: Code Example Consistency Standard

**Context**: Lateral Movement section mixes Python and JavaScript in vulnerable code example (same slide). This reduces clarity and forces context-switching.

**Decision**: 
> Each code example should use **one language per slide**. If a technique applies to multiple languages, use separate slides or a clear "Language: X" label.

**Rationale**:
- Audience can focus on technique, not language switching
- Readers can quickly find examples in their language of choice
- Current mixing in Lateral Movement is confusing

**Implementation**:
- Refactor Lateral Movement section:
   - Slide: Vulnerable service-to-service (Python only)
   - Slide: Vulnerable service-to-service (JavaScript only)
   - Slide: Defended zero-trust (Python only)
- For deck-wide rule: keep code examples monolingual per slide
- Exception: "Language comparison" slides (like "Bad Secrets Management" slide 29) are allowed with clear language labels

**Owner**: McManus  
**Timeline**: Week 1 of expansion phase  
**Affected Slides**: 46–48, 29 (review)

---

## Decision 5: Add Visual Heatmap for Developer Responsibility

**Context**: The deck doesn't visually show which techniques are "developer responsibility" vs. "security ops" vs. "shared."

**Decision**: 
> Create a "Tactic Responsibility Matrix" heatmap showing developer involvement by tactic.

**Rationale**:
- Helps developers quickly identify what they should focus on
- Sets expectations: "Not all of ATT&CK is your job"
- Provides scope clarity for threat modeling workshops

**Matrix Design**:
```
              Initial Exec Persist Priv  Defense Cred   Discovery Lateral Collection C2   Exfil   Impact
Developer     HIGH   HIGH   HIGH   HIGH   HIGH     HIGH   HIGH      MED     HIGH       LOW    HIGH    HIGH
SecOps        MED    MED    MED    MED    HIGH     MED    MED       HIGH    MED        HIGH   MED     HIGH
Shared        HIGH   MED    HIGH   HIGH   MED      MED    MED       HIGH    MED        MED    MED     HIGH
```

**Implementation**:
- New slide after "Implementation Roadmap"
- Mermaid heatmap or HTML table with color coding
- Explanation: "Red = you own this. Yellow = shared responsibility. Gray = primarily security ops."

**Owner**: McManus (design assistance optional)  
**Timeline**: Week 2 of expansion phase  
**Output**: 1 new slide + visual asset

---

## Decision 6: Speaker Notes Template (Standard)

**Decision**: All speaker notes follow this structure for consistency:

```markdown
<!--
SPEAKER NOTES: [Technique ID] [Technique Name]

WHY THIS MATTERS:
- [Business impact: data, availability, compliance]
- [Common attack chain positioning]
- [Incident frequency/severity from threat intel]

REAL-WORLD EXAMPLE:
- [Case study 1: company + year + brief description]
- [Case study 2: company + year + brief description]

AUDIENCE Q&A TALKING POINTS:
- Q: [Common question]
  A: [Practical answer with actionable guidance]
- Q: [Common question]
  A: [Practical answer with actionable guidance]

DELIVERY NOTES:
- [Pacing: 1–2 min typical]
- [Where to pause for questions]
- [Key emphasis points]
- [Difficult concepts to clarify]

RESOURCES:
- [MITRE ATT&CK link]
- [Recommended tools/libraries]
-->
```

**Owner**: McManus  
**Timeline**: Applied to all new and existing slides

---

## Decision 7: Priority Ranking for Expansion

**Context**: We've identified many gaps. Need to sequence work to maximize impact.

**Decision**: 
> Expansion prioritized as:
> 1. **BLOCKING**: Add speaker notes to all 71 slides (required for live delivery)
> 2. **P1**: Complete tactic coverage (add 5–7 slides)
> 3. **P2**: Fix Lateral Movement clarity (improve existing 3 slides)
> 4. **P3**: Add closure/recap slides (3–4 slides)
> 5. **P4**: Visual enhancements (heatmaps, responsibility matrix)

**Owner**: McManus  
**Timeline**: 
- BLOCKING: Weeks 1–2
- P1–P2: Weeks 2–3
- P3: Week 3
- P4: Week 4 (optional, time-permitting)

---

## Decision 8: Marp Build & Delivery Standard

**Context**: Slides are in Markdown (Slides.md) with custom theme. Need clarity on delivery format.

**Decision**: 
> Deck will be delivered as:
> - **Primary**: Live presentation via Marp CLI (HTML/web view) or Marp for VS Code
> - **Secondary**: PDF export for sharing/archival
> - **Backup**: GitHub Pages hosted version (for async audience)

**Implementation**:
- Test Marp CLI: `marp slides/Slides.md --html --output dist/`
- Generate PDF: `marp slides/Slides.md --pdf --output slides.pdf`
- Verify all diagrams render correctly in all formats
- Check theme application (custom-default.css)

**Owner**: Infrastructure/Chris (validation)  
**Timeline**: Before first live presentation  

---

## Decision 9: Slide Counts & Scope Boundaries

**Context**: Current deck is 71 slides. Expansion could balloon it to 100+. Need boundaries.

**Decision**: 
> Target expanded deck: **80–85 slides** (max 90).
> - Original: 71 slides
> - Add: 5–7 tactic expansion slides
> - Add: 3–4 closure/recap slides
> - Refine: 3–5 existing slides for clarity
> - Goal: Professional depth without overwhelming (60–75 min delivery time)

**Out of Scope** (addressed in different project):
- Multi-language code examples for every technique (pick highest-impact)
- Deep-dive research papers on each technique (link to MITRE instead)
- Automated red team simulation code (advanced workshop topic)

**Owner**: McManus  
**Timeline**: Used to gate expansion work  

---

## Decision 10: Next Presenter Handoff

**Context**: This is Chris's deck, but it should be presentable by others.

**Decision**: 
> Speaker notes + deck structure must enable **another presenter to deliver 80% as effectively** as Chris.

**Implementation**:
- Speaker notes include all key talking points, not just speaker cues
- Code examples have explanatory comments (already done)
- Difficult concepts have 1–2 sentences of context in speaker notes
- Delivery timing notes help pacing
- Contact info for questions: Chris's email + GitHub discussions link

**Owner**: McManus (notes authoring)  
**Timeline**: Ongoing as notes are added  

---

## Summary: Decision Table

| Decision | Status | Owner | Timeline | Blocking? |
|----------|--------|-------|----------|-----------|
| 1. Speaker Notes Mandatory | 🔴 TODO | McManus | Weeks 1–2 | ✅ YES |
| 2. Complete 14 Tactics | 🟡 PLANNED | McManus | Weeks 2–3 | ⚠️ Partial |
| 3. Narrative Closure | 🟡 PLANNED | McManus | Week 3 | No |
| 4. Code Consistency | 🟡 PLANNED | McManus | Week 1 | No |
| 5. Responsibility Heatmap | 🟡 PLANNED | McManus | Week 2 | No |
| 6. Speaker Notes Template | ✅ DECIDED | McManus | Ongoing | N/A |
| 7. Expansion Priority | ✅ DECIDED | McManus | Reference | N/A |
| 8. Marp Delivery Standard | ✅ DECIDED | Chris | Before presentation | N/A |
| 9. Slide Count Boundary | ✅ DECIDED | McManus | Reference | N/A |
| 10. Presenter Handoff Readiness | ✅ DECIDED | McManus | Ongoing | N/A |

---

## Next Actions

**Immediate** (this week):
1. McManus: Start drafting speaker notes for slides 1–20
2. McManus: Create new slides for Reconnaissance tactic (3 slides)
3. McManus: Create new slides for Resource Development tactic (2 slides)

**This Week** (continuation):
4. McManus: Complete speaker notes for remaining slides
5. McManus: Refactor Lateral Movement section for clarity
6. McManus: Add closure slides (Coverage Matrix, What We Didn't Cover, 90-Day Roadmap)

**Next Week**:
7. McManus: Create responsibility heatmap slide
8. Chris: Review updated deck, provide feedback
9. Chris: Test Marp rendering and PDF export

**Before Presentation**:
10. Chris + McManus: Dry run with speaker notes
11. Refine pacing based on delivery

---

**Approval**: McManus ✓  
**Status**: Ready for implementation  
**Version**: 1.0 (2026-02-22)


---

### 2026-02-27: User directive — model preference
**By:** Chris Ayers (via Copilot)
**What:** Always use Claude Opus 4.6 1m (`claude-opus-4.6-1m`) for all agent spawns
**Why:** User request — captured for team memory


---

### 2026-02-28: Added MITRE organization overview slides before ATT&CK introduction
**By:** McManus
**What:** Inserted 3 new slides between the OWASP overview and "What is MITRE ATT&CK?" slide: (1) What is MITRE? — the corporation, FFRDCs, mission; (2) MITRE's Cybersecurity Ecosystem — Mermaid diagram showing CVE/CWE/CAPEC/ATT&CK/D3FEND/ATLAS relationships; (3) Why MITRE Matters for Developers — bridging organizational context to developer relevance.
**Why:** The deck jumped from OWASP directly to ATT&CK with no context about MITRE itself or its broader ecosystem. Audiences unfamiliar with MITRE beyond ATT&CK miss the credibility and interconnection story. The new slides create a natural narrative arc: familiar standard (OWASP) → credible organization (MITRE) → ecosystem context → specific framework (ATT&CK). The Mermaid diagram showing framework relationships is especially valuable — it surfaces that developers already consume MITRE data (CVEs, CWEs) through existing tools.

---

# Decision: Full Deck Review — Issues Requiring Resolution

**Date:** 2026-02-27  
**Author:** Kobayashi  
**Status:** Complete — all issues resolved by McManus & Fenster  
**Triggered by:** Comprehensive slide deck review

---

## Critical Issues (Fixed)

### 1. User Enumeration Content Redundancy
**Discovery section** (T1087, lines 1148-1195) and **Reconnaissance section** (T1589, lines 1719-1779) both demonstrate the same vulnerability: login endpoint returning different errors for "user not found" vs "wrong password." The code patterns are nearly identical.

**Resolution:** McManus replaced the login example in Reconnaissance with a different T1589 pattern and added cross-reference to Discovery section.

**Status:** ✅ FIXED

### 2. "What We Covered" Table Missing Supply Chain
The summary table (line 2080) listed 13 tactics but omitted Supply Chain, which has a full 6-slide section. The speaker note falsely claimed "The only tactic we didn't deep-dive is Supply Chain."

**Resolution:** McManus added a Supply Chain row (`T1195, T1195.001 | Dependency verification, integrity validation`) and updated the speaker note to say "all 14 tactics."

**Status:** ✅ FIXED

### 3. Agenda Slide Says "11" — Should Be "13"
Line 44: "11 Technique Categories Across the Kill Chain." The deck now covers 13 tactics. Speaker note also said "11 tactic categories."

**Resolution:** McManus updated to "13 Tactic Categories Across the Kill Chain" and updated speaker note.

**Status:** ✅ FIXED

### 4. T1046 Name Mismatch
Listed as "Network Service Scanning" (line 1139) but official ATT&CK name is "Network Service Discovery."

**Resolution:** McManus corrected the name in the slide.

**Status:** ✅ FIXED

### 5. DEMOS Placeholder
Unresolved placeholder text in deck.

**Resolution:** McManus removed/replaced the placeholder.

**Status:** ✅ FIXED

---

## Important Issues — Technique ID Corrections (Fenster Verification)

### Issue 6: T1185 vs T1539 for Session Cookie Theft

**Kobayashi's Flag:** T1185 (Browser Session Hijacking) may be incorrect for session cookie theft examples.

**Fenster's Verification:** YES, change required. T1185 describes man-in-the-browser attacks (process injection). Session cookie theft is T1539 (Steal Web Session Cookie).

**Corrections Required (16 replacements):**
- Line 630: Comment and table reference
- Lines 634, 642, 651–653, 675, 682–691, 697: Comments in code examples
- Lines 1927, 2125, 2135: "What We Covered" table and speaker notes

**Resolution:** McManus applied all 16 replacements.

**Status:** ✅ FIXED

### Issue 7: SSRF → ATT&CK Mapping

**Kobayashi's Flag:** T1090/T1572 mapping may be conceptually weak for SSRF.

**Fenster's Verification:** YES, change required. SSRF is exploiting a public-facing application (T1190), not a C2 proxy/tunneling technique. T1090/T1572 describe hiding adversary communication, not application exploitation.

**Corrections Required (1 replacement):**
- Line 386: `T1090 (Proxy), T1572 (Protocol Tunneling)` → `T1190 (Exploit Public-Facing Application)`

**Resolution:** McManus applied the correction.

**Status:** ✅ FIXED

---

## Observations (No Action Required)

- **Front-loading (19 slides before code):** Acceptable given the Mermaid diagrams keep it visual.
- **Resource Development and C2 sections are thin (2 slides each):** Expected—limited developer-level control.
- **Attack chain and Crooked Line placement:** Rhetorically sound.
- **Speaker notes quality:** Consistently strong.

---

## Overall Assessment

**Rating: 4/5**

The deck delivers on its "Beyond OWASP" promise. All critical issues have been resolved. The deck is presentation-ready.

---

---

# Decision: Attack Chain Diagram Color Standards

**Date:** 2026-02-28  
**Author:** McManus  
**Status:** Complete — standard defined for all future attack chain diagrams

---

## Standard Color Palette

All attack chain flowchart diagrams use consistent color-coded gradient to indicate attack progression:

| Color | Hex | ATT&CK Association | Usage |
|-------|-----|-------------------|-------|
| Red | #e74c3c | Initial Access / Exploit | Attack entry points |
| Orange | #e67e22 | Execution | Command execution, script injection |
| Yellow | #f39c12 | Credential Access | Credential theft, brute force |
| Green | #2ecc71 | Lateral Movement / Valid Accounts | Privilege expansion, lateral moves |
| Blue | #3498db | Discovery | Reconnaissance, enumeration |
| Purple | #9b59b6 | Collection / Manipulation | Data gathering, tampering |
| Dark (#1a1a2e with #e94560 stroke) | #1a1a2e / #e94560 | Impact / Exfiltration | Final stage impacts |

**Crooked Line Looping Arrows:** Use red (#e94560) linkStyle for highlighting the recursive attack cycle concept.

---

## Rationale

Visual consistency across attack chain diagrams helps the audience build intuition — they learn to associate colors with ATT&CK tactic categories. This also keeps diagram styles cohesive with the custom-default theme's dark aesthetic.

---

## Application

All future attack chain slides must follow this palette. Existing diagrams in the deck already comply.

