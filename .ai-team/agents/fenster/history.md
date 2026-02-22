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
