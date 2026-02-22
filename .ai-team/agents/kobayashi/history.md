# Project Context

- **Owner:** Chris Ayers (clayers@gmail.com)
- **Project:** MITRE ATT&CK for Developers — deep-dive research into ATT&CK framework, Marp slide decks, and multi-language code samples (Python, .NET, JavaScript) showing attack techniques and defenses
- **Stack:** Marp (Markdown slides), Python, .NET/C#, JavaScript, Mermaid diagrams
- **Created:** 2026-02-22

## Learnings

### 2026-02-22: Deep Dive Research Audit Complete

**Project Structure**:
- `slides/Slides.md` — 1531 lines, Marp-formatted presentation covering 11 of 14 ATT&CK tactics
- `samples/python/` — 6 code samples (credential stuffing, command injection, deserialization, logging, data access, secrets)
- `samples/dotnet/` — 5 code samples (command injection, session security, logging, secrets, web shell detection)
- `samples/javascript/` — 6 code samples (SQL injection, session, credential stuffing, supply chain, exfiltration, secrets)

**Coverage Analysis**:
- **Full Coverage (8 tactics)**: Initial Access, Execution, Persistence, Privilege Escalation, Credential Access, Defense Evasion, Discovery, Lateral Movement
- **Partial Coverage (3 tactics)**: Collection, Impact, Supply Chain (under Initial Access)
- **Missing (3 tactics)**: Reconnaissance, Command & Control, Resource Development
- **Critical Gap**: Impact section ends abruptly at line 1194 with technique table but no ransomware/data destruction defenses

**Key Finding**: Current slides excel at isolated technique demonstration but lack cross-tactic attack chain narratives. Real attackers chain techniques (e.g., T1190→T1059→T1505.003→T1021→T1213). Research plan prioritizes 5 realistic attack scenarios.

**Architecture Decision**: Expand slides to ~2200 lines with:
1. P0 tasks: Complete Reconnaissance, C2, Impact sections (+20 slides, +8 samples)
2. P1 tasks: Add 5 attack chain scenarios (+20 slides, +10 samples)
3. P2 tasks: Go/Rust samples, mobile, CI/CD content (optional)

**File Paths**:
- Research plan: `.ai-team/decisions/inbox/kobayashi-research-plan.md`
- Slide deck: `slides/Slides.md`
- Code samples: `samples/{python,dotnet,javascript}/`

<!-- Append new learnings below. Each entry is something lasting about the project. -->
