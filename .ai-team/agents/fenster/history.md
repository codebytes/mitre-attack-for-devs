# Project Context

- **Owner:** Chris Ayers (clayers@gmail.com)
- **Project:** MITRE ATT&CK for Developers — deep-dive research into ATT&CK framework, Marp slide decks, and multi-language code samples (Python, .NET, JavaScript) showing attack techniques and defenses
- **Stack:** Marp (Markdown slides), Python, .NET/C#, JavaScript, Mermaid diagrams
- **Created:** 2026-02-22

## Learnings

<!-- Append new learnings below. Each entry is something lasting about the project. -->

### 2025-02-21: ATT&CK Research Document Created

**Task:** Created comprehensive ATT&CK research document for developer audience.

**Output:** `.ai-team/agents/fenster/attack-research.md` — 44KB reference document covering:
- All 14 ATT&CK tactics with developer relevance context
- 15 priority technique deep dives (T1190, T1059, T1078, T1195, T1552, T1070, T1110, T1567, T1499, T1565, T1098, T1134, T1505.003, T1021, T1213)
- OWASP Top 10 2025 → ATT&CK mapping table
- 5 modern attack chain scenarios
- D3FEND defensive technique mappings
- Emerging techniques section (AI/ML, cloud-native, API, container, CI/CD attacks)

**Key Insights:**
- Existing slides (Slides.md) already cover 11 technique categories with code examples—research document provides deeper context and additional techniques
- Developer-centric framing is critical: emphasized application-layer concerns, code-level defenses, and practical mitigations
- OWASP bridge essential: developers understand vulnerabilities better than adversary tactics, so mapping between the two frameworks increases accessibility
- Attack chains demonstrate technique sequencing: showing how techniques combine (e.g., T1195 → T1552 → T1078 → T1098) illustrates real-world attacker behavior
- Modern development practices dominate: microservices, containers, cloud, CI/CD are where developers operate—research focused there

**Research Approach:**
- Started by reviewing existing slides to avoid duplication and identify gaps
- Prioritized techniques based on developer-controllable defenses (excluded network/host-layer techniques)
- Structured each tactic with "why developers should care" to establish relevance immediately
- Used consistent format for technique deep dives: what/how attackers use/how developers defend
- Mapped to OWASP Top 10 2025 to leverage existing developer knowledge base
- Created realistic attack chains showing multi-technique sequences (not single isolated techniques)

**Coverage Decisions:**
- **Included:** Application-layer techniques, API/web security, authentication/authorization, data protection, logging, supply chain
- **De-emphasized:** Network-layer techniques (mostly outside developer control), phishing (user-focused), hardware exploits
- **Emerging areas:** AI/ML security, cloud metadata exploitation, GraphQL attacks, container escape, CI/CD pipeline compromise

**Terminology:**
- Consistently used T-codes (e.g., T1190) with technique names
- Mapped to D3FEND defensive IDs where applicable
- Referenced tactic IDs (TA0001-TA0043) for completeness
- Used OWASP category names developers recognize (Broken Access Control, Injection, etc.)

**Document serves as:**
- Reference for slide content development (McManus can extract key points)
- Source material for code examples (Hockney can reference defensive patterns)
- Threat modeling input for security-focused development
- Training foundation for developer security education

**Maintenance:** Document should be updated quarterly as ATT&CK framework evolves (new techniques, deprecated techniques, updated mitigations).

📌 Team update (2026-02-27): Always use 'claude-opus-4.6-1m' model for all agent spawns — decided by Chris Ayers (Copilot)

### 2025-07-17: Technique ID Verification (Kobayashi Review)

**Task:** Verified two technique ID issues flagged in Kobayashi's deck review.

**Findings:**

1. **T1185 → T1539 (CONFIRMED CHANGE NEEDED):** The slide deck used T1185 (Browser Session Hijacking) for session cookie theft scenarios. T1185 is specifically about man-in-the-browser attacks — adversaries injecting into browser processes to pivot through authenticated sessions (Cobalt Strike browser pivoting, Dridex, etc.). The slides describe cookie theft via XSS, insecure flags, and session replay — this maps to T1539 (Steal Web Session Cookie). 16 occurrences across the deck need correction.

2. **SSRF mapping T1090/T1572 → T1190 (CONFIRMED CHANGE NEEDED):** The OWASP-to-ATT&CK mapping table mapped SSRF to T1090 (Proxy) and T1572 (Protocol Tunneling). Both are Command & Control techniques about hiding adversary communications. SSRF is an exploitation technique — it maps to T1190 (Exploit Public-Facing Application). MITRE's own T1190 docs cite web app vulnerabilities including SSRF as examples.

**Key Learnings:**
- T1185 vs T1539 is a common confusion point. T1185 = browser process injection/pivoting (post-exploitation, requires malware). T1539 = cookie theft and replay (can be enabled by application-level flaws like missing httpOnly/secure flags).
- ATT&CK mapping should reflect what the adversary is *doing* (the technique), not the incidental *effect* of the exploit. SSRF makes a server act like a proxy, but the technique is exploitation of a public-facing app.
- CISA's mapping best practices: map to observed initial behavior and intent, not downstream mechanics.
- Always cross-reference the actual MITRE ATT&CK technique pages when reviewing T-codes — the technique names can be misleading without reading the full description.

**Output:** `.ai-team/decisions/inbox/fenster-technique-id-verification.md` — full findings with line-by-line correction table for McManus.
