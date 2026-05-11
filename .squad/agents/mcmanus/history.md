# McManus — History

## Core Context

- **Project:** A Marp slide deck teaching developers the MITRE ATT&CK framework with code examples.
- **Role:** Content Writer
- **Joined:** 2026-05-11T15:55:39.699Z

## Learnings

<!-- Append learnings below -->
- 2026-05-11: Applied Supply-Chain Case Study Narrative Arc to slides/Slides.md. Added 3 new slides: (1) "The Supply-Chain Attack Arc" table (lines ~709–723, replaced old "Supply Chain Attack Examples" bullet list) — walks through event-stream → Shai-Hulud → Notepad++ → Axios → Log4Shell → SolarWinds/XZ nation-state row; (2) "Case Study: Notepad++ Update Hijack (2025)" (lines ~724–752, inserted before XZ Utils) — 5-step attack chain with ATT&CK T-IDs T1195.002/T1036/T1574.002/T1140/T1071.001, Chrysalis backdoor facts from dossier; (3) "Log4Shell (2021) — Dependency-Trust Failure, Not Compromise" (lines ~813–845, inserted after Axios) — framed as dependency-trust failure vs. supply-chain compromise, CVE-2021-44228, CVSS 10.0, first visible-content SBOM expansion ("Software Bill of Materials (SBOM) visibility"). Section intro speaker note updated to remove Log4Shell from "supply-chain" framing. Marp HTML build passed with exit 0.
- 2026-05-11: Applied acronym-first-use convention to slides/Slides.md. Expanded 4 acronyms in visible slide content: C2 (line 192, SolarWinds kill-chain bullet), RCE + CVSS together (line 740, XZ Utils ATT&CK techniques bullet — same bullet handled both), RAT (line 756, Axios case study numbered list), SIEM (line 1018, Implementation Roadmap Phase 2 bullet). SBOM, SAST, CVE, and RBAC appeared only in code blocks, code comments, or speaker notes — no visible-content expansion needed. Edge case: line 740 carried both RCE and CVSS — expanded both inline without splitting the bullet. Marp HTML build passed with exit 0.
- 2026-05-11: Acronym audit found the main deck defines TTPs and FMX inline, but many security-specific acronyms are first used bare in slides or speaker notes. Strong candidates for first-use expansion include ATT&CK, SIEM, SBOM, SAST, CVE/CVSS, RCE, RAT, C2, SAML, RBAC, IAM, CSRF, XSS, and SQLi.
- 2026-05-11: Medieval/fantasy narrative works best as a threaded motif in section intros and speaker notes, especially castle-defense analogies for Initial Access, Persistence, Credential Access, Defense Evasion, Exfiltration, and Defense in Depth. Avoid applying it to code samples, MITRE matrix/mapping tables, and CVE-specific facts.
- 2026-05-11: Supply-chain research found Axios 2026 and Notepad++ 2025/2026 are well-documented enough for deck use. Strongest Notepad++ angle is update-infrastructure hijack/Chrysalis, not generic fake installers. Shai-Hulud is the strongest modern npm narrative; Log4Shell should be framed as dependency-trust failure, not malicious supply-chain compromise.
