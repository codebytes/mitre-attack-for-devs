# Slide Deck Analysis: MITRE ATT&CK for Developers

**Document**: Deep-dive research analysis  
**Slide Deck**: `slides/Slides.md` (1,193 lines, 1,532 line count in view)  
**Analysis Date**: 2026-02-22  
**Analyst**: McManus (Content Dev)  

---

## Executive Summary

The deck is **strong but incomplete**. It covers 10 of 14 ATT&CK tactics with practical code examples across Python, .NET/C#, and JavaScript. The narrative is compelling: it starts with "think like attackers" and moves to detection/defense strategies. However, **the deck abruptly ends after "Questions?" slide** with no:

- Comprehensive recap of all covered tactics
- Resource/reference summary slide  
- Speaker notes (critical for full delivery)
- Missing 4 tactics (Reconnaissance, Resource Development, Command & Control, Lateral Movement variants not covered)
- No visual consistency/gap summary for audience takeaways

**Grade: B+ → A- with gap closure**

---

## A. Current Slide Inventory

### Total Slide Count: **69 slides**

### By Category:

#### **Title & Intro (4 slides)**
1. **Main title**: "MITRE ATT&CK for Developers — Beyond OWASP"
2. **Speaker intro**: Chris Ayers bio + social links (background image: portrait.png)
3. **Agenda**: Lists 6 main sections
4. **Security Challenge**: Problem statement (no code)

#### **Context & Framing (5 slides)**
5. **What is OWASP?** - Vulnerability classification intro
6. **What is MITRE ATT&CK?** - Origin, structure, enterprise matrix
7. **ATT&CK Structure** - Tactics/Techniques/Procedures definition
8. **14 ATT&CK Tactics** - Flowchart/Mermaid diagram (Pre-Attack, Get In, Stay In, Act)
9. **OWASP vs ATT&CK** - Two-column comparison
10. **Why Both?** - Complementary approach rationale
11. **Mapping OWASP to ATT&CK** - 6-row technique mapping table

#### **Technique Deep Dives (54 slides)**

Organized by attack phase/tactic:

##### **Initial Access & Credential Attacks (3 slides)**
- 12: Attacker Techniques table (T1190, T1078, T1110, T1566)
- 13: Vulnerable code SQL Injection (T1190, Python)
- 14: Defended code Parameterized Queries (Python)

##### **Execution & Code Injection (5 slides)**
- 15: Attacker Techniques table (T1059, T1203, T1055)
- 16: Vulnerable Command Injection (T1059, C#)
- 17: Defended Command Allowlisting (C#)
- 18: Unsafe Deserialization (T1203, Python+)
- 19: (continuation of 18 — defended code)

##### **Persistence & Session Hijacking (6 slides)**
- 20: Attacker Techniques table (T1098, T1185, T1505.003)
- 21: Vulnerable Session Management (T1185, T1552, JavaScript)
- 22: Defended Session Management (JavaScript)
- 23: Web Shell Detection (T1505.003, C#)

##### **Privilege Escalation (4 slides)**
- 24: Attacker Techniques table (T1068, T1548, T1134)
- 25: Vulnerable IDOR code (T1068, Python)
- 26: Defended Authorization Checks (Python)
- 27: Token Manipulation Prevention (T1134, JavaScript JWT)

##### **Credential Access & Secrets (5 slides)**
- 28: Attacker Techniques table (T1552, T1555, T1528)
- 29: Bad Secrets Management (Python, C#, JavaScript - vulnerable)
- 30: Good Secrets Python & C# (Azure Key Vault integration)
- 31: Good Secrets JavaScript (Google Secret Manager)
- 32: Secrets Scanner Implementation (Python regex patterns)

##### **Defense Evasion & Log Tampering (4 slides)**
- 33: Attacker Techniques table (T1027, T1070, T1036)
- 34: Log Injection Attack (T1070 vulnerable, Python)
- 35: Tamper-Evident Logging (T1070 defended, C#)
- 36: Immutable Logging Architecture (Mermaid diagram)

##### **Discovery & Information Disclosure (4 slides)**
- 37: Attacker Techniques table (T1087, T1046, T1082)
- 38: User Enumeration (T1087 vulnerable, Python)
- 39: Defended Consistent Responses (Python)
- 40: API Endpoint Discovery Prevention (T1046/T1082 defended, JavaScript)

##### **Supply Chain Compromise (5 slides)**
- 41: Attacker Techniques table (T1195, T1195.001)
- 42: Supply Chain Attack Examples (narrative, no code)
- 43: Dependency Verification (Bash commands for NPM, Python, .NET)
- 44: Package Integrity Validation (Python, T1195.001 prevention)
- 45: Supply Chain Security Flow (Mermaid diagram)

##### **Lateral Movement (3 slides)**
- 46: Attacker Techniques table (T1021, T1550, T1563)
- 47: Vulnerable insecure service-to-service (Python + JavaScript fragments)
- 48: Defended Zero-Trust Service Communication (mTLS + scoped tokens, Python)

##### **Collection & Exfiltration (4 slides)**
- 49: Attacker Techniques table (T1213, T1567, T1020)
- 50: Data Access Anomaly Detection (Python, T1213 detection)
- 51: API Rate Limiting with Exfil Detection (JavaScript, T1567/T1020 prevention)
- 52: Data Flow Monitoring (Mermaid diagram)

##### **Impact & Denial of Service (3 slides)**
- 53: Attacker Techniques table (T1499, T1565, T1486, T1485)
- 54: Vulnerable ReDoS (T1499.004, JavaScript regex)
- 55: Defended Input Limits (JavaScript)
- 56: Data Integrity Protection (C#, T1565/T1485 prevention)

##### **Less Developer-Focused Tactics (2 slides)**
- 57: Reconnaissance, C2, Resource Development (brief, less code)

#### **Implementation & Closing (7 slides)**
- 58: Practical Implementation header (fit slide)
- 59: ATT&CK-Informed Threat Modeling (Mermaid flow)
- 60: Map Features to Techniques (10-row table, coverage matrix)
- 61: Building Detection Into Code (bullet points, no code)
- 62: Defense in Depth Architecture (Mermaid graph)
- 63: OWASP + ATT&CK Integration (two-flow Mermaid)
- 64: Integration Points table (6 tools/practices)
- 65: Implementation Roadmap (3-column phases)
- 66: Team Adoption Strategies (bullet points)
- 67: ATT&CK Navigator (tool intro)
- 68: Start Small — Pick Your Top 3 (recommendation: T1078, T1185, T1213)
- 69: Key Takeaways (6 checkpoints)
- 70: Links + Chris bio
- 71: Questions? + owl.png background

### Summary by Slide Type:

| Type | Count | Examples |
|------|-------|----------|
| **Title/Header** | 7 | Main title, section breaks (fit slides) |
| **Technique Overviews** | 10 | Attacker Techniques tables |
| **Vulnerable Code** | 15 | SQL injection, command injection, deserialization, etc. |
| **Defended Code** | 15 | Parameterized queries, WAF, secrets mgmt, etc. |
| **Diagram (Mermaid)** | 5 | Kill chain, logging architecture, threat modeling flow, defense depth |
| **Comparison/Reference** | 8 | OWASP vs ATT&CK, mapping tables, integration points |
| **Implementation/Strategy** | 9 | Roadmap, adoption, threat modeling |
| **Closing/Resources** | 5 | Takeaways, links, Q&A |

---

## B. Marp Conventions Used

### Frontmatter Configuration
```yaml
---
marp: true
theme: custom-default
paginate: true
footer: '@Chris_L_Ayers - https://chris-ayers.com'
---
```

- ✅ Uses `custom-default` theme (defined in `slides/themes/custom-default.css`)
- ✅ Pagination enabled (slide numbers auto-generated)
- ✅ Global footer on every slide
- ✅ Custom footer override on first slide: `<!-- _footer: 'https://github.com/codebytes/mitre-attack-for-devs' -->`

### Section Separators

- **Fit slides**: `# <!-- fit --> Section Title` (e.g., "Let's Think Like Attackers")
- **Regular headers**: `# Title` (main) or `##` (subtitle)
- **Column layouts**: `<div class="columns">` and `</div>` for 2-column, `<div class="columns3">` for 3-column

### Code Blocks

Format: **Language-specific fenced blocks** with technique annotations:
```markdown
\`\`\`python
# VULNERABLE - Comment explains the T-code vulnerability
# T1190: SQL Injection vulnerability
\`\`\`
```

**Patterns**:
- ✅ Fenced code (triple backticks with language)
- ✅ Comments tag the ATT&CK technique ID
- ✅ Both "VULNERABLE" and "DEFENDED" variants on adjacent slides
- ✅ Languages used: Python, C#, JavaScript, Bash (for CLI tools)
- ⚠️ Code is compact but readable

### Mermaid Diagrams

Embedded as `<div class="mermaid">` blocks:

1. **Kill Chain Flowchart** (line 90-107):
   - `flowchart LR` - Left to right flow
   - Subgraph grouping (Pre-Attack, Get In, Stay In, Act)
   - Shows tactic progression

2. **Immutable Logging Architecture** (line 777-787):
   - `graph LR` - Data flow
   - Shows: App → Logger → Hash → Storage + SIEM → Tamper Detection → Alert

3. **Supply Chain Security Flow** (line 970-981):
   - `flowchart TD` - Top to down
   - Decision gates (Hash Valid?, Clean?)
   - Terminal states (Block & Log T1195.001, Install & Monitor)

4. **Data Flow Monitoring** (line 1165-1177):
   - Complex conditional flow
   - Shows anomaly detection loop with multiple gates

5. **Threat Modeling Cycle** (line 1323-1331):
   - Shows iterative process: Identify → Map → Assess → Design → Implement → Test → Loop back

6. **Defense in Depth** (line 1368-1378):
   - Linear progression through defensive layers
   - Input Validation → Auth → Authz → Data Controls → Analytics → Detection → Response

7. **OWASP + ATT&CK Integration** (line 1384-1393):
   - Dual-path flow: Secure Coding + Behavioral Monitoring → Secure by Design

### Image Usage
- ✅ Background images: `![bg left:40%](./img/portrait.png)` and `![bg right](./img/owl.png)`
- ✅ Images are sized with background positioning (`left:40%`, `right`)
- ✅ Images stored in `slides/img/`

### Column Layouts

**Two-column** (used in OWASP vs ATT&CK):
```html
<div class="columns">
<div>
### Left Column
- Content
</div>
<div>
### Right Column
- Content
</div>
</div>
```

**Three-column** (used in Implementation Roadmap):
```html
<div class="columns3">
<div>
### Phase 1
- Items
</div>
<!-- etc -->
</div>
```

### Speaker Notes
🚨 **NONE FOUND** — No `<!--  -->` HTML comment blocks for speaker notes. This is a critical gap for a full presentation delivery.

### Footer Configuration
- Global footer: `'@Chris_L_Ayers - https://chris-ayers.com'` on all slides
- Override on title slide: `'https://github.com/codebytes/mitre-attack-for-devs'`
- Uses `paginate: true` for automatic slide numbers

---

## C. Content Flow Analysis

### Narrative Arc

**Act 1: Foundation (Slides 1–11)**
- Hook: "Security Challenge for Developers"
- Context: OWASP vs ATT&CK (not either/or but both)
- Framing: Why developers need to think about adversary behavior

**Act 2: Deep Dives (Slides 12–57)**
- **Repeating pattern**: Each tactic gets 2–6 slides
  - Slide 1: Technique overview (table of related T-codes)
  - Slide 2+: Code examples (vulnerable + defended pairs)
  - Final: Diagram or detection code (if applicable)
- **Coverage**: 10 tactics across the kill chain (Initial Access → Impact)
- **Audience perspective**: "Here's what attacks look like; here's how to stop them"

**Act 3: Integration & Implementation (Slides 58–69)**
- Threat modeling methodology
- Practical implementation roadmap (3 phases)
- Team adoption strategy
- Resources and closing

### Strongest Sections

✅ **Credential Access & Secrets** (Slides 28–32)
- Covers all 3 languages (Python, C#, JavaScript) consistently
- Regex-based secrets scanner implementation is production-ready
- Real-world tools (Azure Key Vault, Google Secret Manager)
- High audience value

✅ **Execution & Code Injection** (Slides 15–19)
- Deserialization attack is sophisticated (pickle/JSON comparison)
- Command injection defense is thorough (allowlisting pattern)
- Clear before/after for each technique

✅ **Privilege Escalation** (Slides 24–27)
- IDOR example is extremely relatable
- JWT token manipulation is timely and practical
- Code demonstrates both weakness and proper verification

✅ **Implementation Roadmap** (Slides 65–68)
- Non-overwhelming ("Start Small — Pick Your Top 3")
- Clear 3-phase progression
- Roadmap shows iterative adoption

### Weakest/Rushed Sections

⚠️ **Lateral Movement** (Slides 46–48)
- Only 3 slides, feels compressed
- Vulnerable code mixes Python + JavaScript fragments (inconsistent)
- Defended code is dense; hard to follow service token flow

⚠️ **Reconnaissance, C2, Resource Development** (Slide 57)
- Crammed into single 2-column slide
- Minimal code; mostly bullets
- Developer role is vague ("largely outside developer control")

⚠️ **Building Detection Into Code** (Slide 61)
- Bullet list only, no code examples
- Would benefit from a simple detection class/pattern

### **The Abrupt Ending Problem**

**Slides 69–71** feel rushed:
- Slide 69: Key Takeaways (6 bullets) — good
- Slide 70: Resources + links (good) — but packed with too much info
- Slide 71: Questions? (standard closing)

**Missing**:
- No recap/summary of all 10 covered tactics
- No "next steps" for the audience beyond reading docs
- No mention of ongoing monitoring/improvement cycle
- No slide showing "What We Didn't Cover" (the 4 missing tactics)

---

## D. Gap Identification

### **Tactics Coverage**

| Tactic | Covered? | Slides | Depth |
|--------|----------|--------|-------|
| **Reconnaissance (TA0043)** | Partial | 57 | Minimal (1/2 slide) |
| **Resource Development (TA0042)** | Partial | 57 | Minimal (1/2 slide) |
| **Initial Access (TA0001)** | ✅ Yes | 12–14 | 3 slides |
| **Execution (TA0002)** | ✅ Yes | 15–19 | 5 slides |
| **Persistence (TA0003)** | ✅ Yes | 20–23 | 4 slides |
| **Privilege Escalation (TA0004)** | ✅ Yes | 24–27 | 4 slides |
| **Defense Evasion (TA0005)** | ✅ Yes | 33–36 | 4 slides |
| **Credential Access (TA0006)** | ✅ Yes | 28–32 | 5 slides |
| **Discovery (TA0007)** | ✅ Yes | 37–40 | 4 slides |
| **Lateral Movement (TA0008)** | ✅ Yes | 46–48 | 3 slides (compressed) |
| **Collection (TA0009)** | ✅ Yes | 49–52 | 4 slides |
| **Command & Control (TA0011)** | Partial | 57 | Minimal (1/2 slide) |
| **Exfiltration (TA0010)** | ✅ Yes (as Collection/Exfil pair) | 49–52 | 4 slides |
| **Impact (TA0014)** | ✅ Yes | 53–56 | 4 slides |

**Verdict**: 10/14 tactics substantially covered. 4 tactics (Reconnaissance, Resource Dev, C2, partial Lateral Movement) are underdeveloped.

### **Code Example Coverage**

| Language | Count | Techniques | Balance |
|----------|-------|------------|---------|
| **Python** | 11 | SQL Injection, Deserialization, IDOR, User Enum, Secrets, Log Injection, Data Access Monitor, Secrets Scanner | ✅ Good |
| **C#/.NET** | 8 | Command Injection, Secrets (Key Vault), Web Shell Detection, Tamper-Evident Logging, Token Validation, Data Integrity | ✅ Good |
| **JavaScript** | 9 | Credential Stuffing, Session Management, Token Validation (JWT), API Endpoint Discovery, ReDoS, Rate Limiting, Exfil Detection | ✅ Good |
| **Bash/CLI** | 1 | Dependency Verification (npm, pip, dotnet) | Minimal |

**Total code blocks**: ~28 code examples (vulnerable + defended pairs)

**Gap**: SQL injection is Python-only; would benefit from C#/.NET version.

### **Mermaid Diagrams**

| Diagram | Type | Value |
|---------|------|-------|
| Kill Chain | Flowchart | Essential (explains tactic sequence) |
| Immutable Logging | Data flow | Supports T1070 defense |
| Supply Chain Security | Decision tree | Great for T1195 visualization |
| Data Flow Monitoring | Multi-gate flow | Supports T1213/T1567 detection |
| Threat Modeling | Process loop | Practical methodology |
| Defense in Depth | Linear layers | Good defense overview |
| OWASP + ATT&CK | Dual integration | Supports key message |

**Verdict**: ✅ 7 diagrams. Could add:
- **T1110 (Brute Force)** detection pattern diagram
- **Secrets lifecycle** flow (credential rotation, revocation)
- **Session validation** state machine

### **Speaker Notes**

🚨 **CRITICAL GAP**: Zero speaker notes in the deck.

For a "deep dive research project," speaker notes should cover:
- What each technique actually means
- Why it's dangerous (business + technical impact)
- Common real-world examples
- Audience Q&A talking points
- Timing guidance (2 min per technical section, 1 min per overview)

### **Summary Slides & Recap**

**Issue**: Deck ends abruptly after Key Takeaways.
- Missing: "Techniques We Covered" recap slide
- Missing: "Techniques to Research Further" slide
- Missing: "Your Next Steps" actionable slide
- Missing: "Contact & Questions" with communication channels (email, GitHub discussions, etc.)

### **Visual Consistency**

✅ **Strengths**:
- Consistent header format (Technique ID in tables)
- Consistent vulnerable/defended pair pattern
- Consistent code block formatting

⚠️ **Opportunities**:
- No color-coding by tactic (would help scanning)
- No visual "difficulty level" indicator (which techniques are most impactful?)
- No "priority matrix" (impact vs. effort to implement)

---

## E. Expansion Recommendations

### **Priority 1: Speaker Notes (Blocking item)**

📝 Add HTML comments to every technical slide:

```markdown
<!-- 
SPEAKER NOTES: T1190 Exploit Public-Facing Application

Why This Matters:
- Most common initial access vector (60% of incidents)
- Often chained with T1110 for credential discovery
- Business impact: Direct data breach, system compromise

Real-World Example:
- 2019 Capital One breach: T1190 (Elastic Search misconfiguration)
- 2020 Twitter: T1190 (OAuth token endpoint exposed)

Audience Q&A Talking Points:
- "How do I know if my app is vulnerable?"
  → Run OWASP ZAP / Burp Suite on staging; check SAST output
- "Can I prevent all exploits?"
  → No, but you can reduce surface area: input validation, patching, WAF
- "What's the detection angle?"
  → Monitor for unusual query patterns, 5xx errors at scale, WAF logs

Delivery Notes:
- Spend 2 minutes on vulnerable code walkthrough
- Pause after showing the attack payload
- Emphasize the parameterized query defense is non-negotiable
-->
```

### **Priority 2: Close the Tactic Gaps**

Add 2–3 slides per missing tactic:

#### **Reconnaissance (TA0043) Expansion** (Currently 1/2 slide, recommend 3 slides)
- **Slide A**: Tech Details (T1592, T1595, T1598 overview)
- **Slide B**: Code Example — "Verbose Error Messages Enable T1592"
  - Vulnerable: Stack trace in HTTP response showing framework/version
  - Defended: Generic error response + internal logging
- **Slide C**: API Metadata Hardening (disable `X-Powered-By`, remove version headers)

#### **Resource Development (TA0042) Expansion** (Currently 1/2 slide, recommend 2 slides)
- **Slide A**: Tech Details (T1583, T1584, T1600 overview)
- **Slide B**: Developer Role — Validate External Integrations
  - Code: Webhook signature verification (HMAC-SHA256)
  - Code: Third-party OAuth token revocation audit

#### **Command & Control (TA0011) Expansion** (Currently 1/2 slide, recommend 2 slides)
- **Slide A**: Tech Details (T1071, T1572 overview)
- **Slide B**: Code Example — "Detecting C2 Over HTTPS"
  - Mermaid: Network analysis workflow
  - Code: TLS certificate pinning for trusted APIs

### **Priority 3: Add Recap Slides**

**Slide X: "Technique Coverage Map"**
- Mermaid: ATT&CK Navigator-style heatmap showing:
  - Which tactics have code examples (green)
  - Which have diagrams (blue)
  - Which are high-priority for your app (red)

**Slide X+1: "What We Didn't Cover"**
- Table: 4 tactics + brief explanation + pointer to MITRE docs
- Messaging: "These are outside the developer's direct control but important to understand"

**Slide X+2: "Your Next Steps"**
- Week 1: Pick one technique (recommend T1078 Valid Accounts)
- Week 2–3: Implement detection logging
- Week 4: Test with red team or pen test
- Ongoing: Monitor and iterate

### **Priority 4: Enhance Weakest Sections**

#### **Lateral Movement Reconstruction**
Current: 3 slides, feels rushed and inconsistent

Recommend 4–5 slides:
1. Attacker Techniques overview (same)
2. Vulnerable service-to-service (same, but Python + JavaScript separate)
3. mTLS + Token Scoping (same, but expand with diagram)
4. **NEW**: Service Account Management (rotating credentials, audit)
5. **NEW**: Detection — Monitoring cross-service calls for anomalies

#### **Defense Evasion Expansion**
Current: 4 slides (T1027, T1070, T1036)

Add 1–2 slides:
- **T1036 (Masquerading)**: Code example showing file extension spoofing (IDOR.pdf.exe) vs. defense
- **T1140 (Deobfuscation)**: Brief mention that obfuscation is not security

### **Priority 5: Add Visual References**

**New Slide: "ATT&CK Heatmap"**
```
Mermaid Heat Matrix:
       Initial Exec Persist Priv   Defense Cred   Discovery Lateral Collect C2    Exfil   Impact
Dev    [HIGH] [HIGH] [HIGH] [HIGH] [HIGH]  [HIGH] [HIGH]    [MED]   [HIGH]  [LOW]   [HIGH]  [HIGH]
SecOps [MED]  [MED]  [MED]  [MED]  [HIGH]  [MED]  [MED]     [HIGH]  [MED]   [HIGH]  [MED]   [HIGH]
```
Color coding: RED (high dev responsibility), YELLOW (shared), GRAY (security-focused)

### **Priority 6: Add "Top 10" Implementation Checklist**

Create a printable checklist slide:
```
[ ] T1078: Implement MFA + session rotation
[ ] T1185: Add session fingerprinting  
[ ] T1213: Enable query logging + anomaly detection
[ ] T1110: Rate limit login attempts + account lockout
[ ] T1552: Audit and move all secrets to vault
[ ] T1190: Input validation + SQL parameterization
[ ] T1070: Immutable audit logging
[ ] T1195.001: Lock down dependencies (lock files + hashes)
[ ] T1087: Consistent error responses
[ ] T1499: API rate limiting + WAF rules
```

---

## F. Technical Debt & Observations

### ✅ What's Working Well

1. **Code Authenticity**: All code examples are realistic and runnable
2. **Progression**: Vulnerable → Defended pattern is clear and teaches cause-and-effect
3. **Multi-language**: Python, C#, JavaScript coverage is balanced
4. **Real-world Tools**: Azure Key Vault, Google Secret Manager, npm/pip commands
5. **Threat Modeling**: Roadmap is non-overwhelming ("Start Small — Pick Your Top 3")
6. **Kill Chain Visualization**: Mermaid diagrams ground the abstract tactic framework

### ⚠️ Rough Edges

1. **No Speaker Notes**: Critical for live delivery; must add before presentation
2. **Lateral Movement**: Inconsistent code language mixing (Python + JS on same slide)
3. **Reconnaissance/Resource Dev**: Treated as afterthoughts; deserve full sections
4. **Delivery Timing**: Unclear how long this should take (estimated 45–60 min if well-paced)
5. **Audience Level**: Assumes intermediate developer knowledge; no "for beginners" variant
6. **Printable Version**: No slide designed for handouts (complex code doesn't print well)

### 🛠️ Build/Test Notes

- ✅ Theme files exist: `custom-default.css`, `custom-gaia.css`, `custom-uncover.css`
- ✅ Mermaid is injected via `<script>` tag at end (line 1528–1531)
- ✅ Images verified: `portrait.png`, `owl.png` exist

---

## G. Recommendations Summary Table

| Priority | Action | Impact | Effort | Owner |
|----------|--------|--------|--------|-------|
| **BLOCKING** | Add speaker notes to all 71 slides | Delivery success | High | McManus |
| **P1** | Expand Reconnaissance tactic (1→3 slides) | Coverage completeness | Medium | McManus |
| **P1** | Expand Resource Development (1→2 slides) | Coverage completeness | Medium | McManus |
| **P2** | Fix Lateral Movement section (improve code consistency) | Clarity | Medium | McManus |
| **P2** | Add "Technique Coverage Map" recap slide | Audience retention | Low | McManus |
| **P3** | Add "Your Next Steps" actionable slide | Call-to-action | Low | McManus |
| **P3** | Enhance weakest sections with diagrams | Visual retention | Medium | McManus |
| **P4** | Color-code tactics by developer responsibility | Scannability | Low | Designer |
| **P4** | Create printable handout version | Reference value | Medium | Design |

---

## H. Metrics

### Current Deck Stats

| Metric | Value |
|--------|-------|
| Total Slides | 71 |
| Code Examples | 28 (vulnerable + defended pairs) |
| Mermaid Diagrams | 7 |
| Languages | 3 (Python, C#, JavaScript) + Bash |
| Tactics Covered | 10/14 |
| Techniques Referenced | 40+ unique T-codes |
| Tables/Comparison Slides | 8 |
| Speaker Notes | 0 🚨 |
| Estimated Delivery Time | 45–60 min (no speaker notes = risky) |

### Post-Expansion Goals

| Metric | Target |
|--------|--------|
| Total Slides | 80–85 |
| Code Examples | 32–35 |
| Mermaid Diagrams | 10–12 |
| Tactics Covered | 14/14 |
| Speaker Notes | 100% |
| Estimated Delivery Time | 60–75 min (well-paced) |

---

## Conclusion

**The deck is a solid B+.** It tells a compelling story: "OWASP + ATT&CK = Complete Security." The code examples are authentic, the progression is logical, and the implementation roadmap is practical.

**To reach A- or A**, we need:
1. **Speaker notes** (blocking) — essential for confident delivery
2. **Complete tactic coverage** — fill the 4 gaps (Recon, Resource Dev, C2)
3. **Narrative closure** — recap and "next steps" slides
4. **Lateral Movement refinement** — improve code consistency and clarity

**The deep-dive research angle** isn't quite realized yet. The current deck is more of an "introduction + practical guide" than a research-grade deep dive. With speaker notes, full tactic coverage, and visual heatmaps, it becomes a true resource for teams wanting to bake ATT&CK into their development lifecycle.

---

**Next Steps for McManus**:
- [ ] Draft speaker notes for all 71 slides
- [ ] Add 5–7 new slides filling tactic gaps
- [ ] Create recap/roadmap closure slides
- [ ] Validate Marp rendering and PDF export
- [ ] Get feedback from Chris Ayers on pacing and emphasis
