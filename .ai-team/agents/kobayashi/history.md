# Project Context

- **Owner:** Chris Ayers (clayers@gmail.com)
- **Project:** MITRE ATT&CK for Developers — deep-dive research into ATT&CK framework, Marp slide decks, and multi-language code samples (Python, .NET, JavaScript) showing attack techniques and defenses
- **Stack:** Marp (Markdown slides), Python, .NET/C#, JavaScript, Mermaid diagrams
- **Created:** 2026-02-22

## Learnings

### 2026-02-22: BUILD ORDER FINALIZED — 7 SEQUENTIAL TASKS

**Decision Made:** Team has 3 days to expand slides from 71→85, add speaker notes, and close all coverage gaps.

**Key Insight:** The project has **3 layers of work**:
1. **Clarity Issues (BLOCKING)**: OWASP-ATT&CK mapping confusion (Keaton Issue #2) must be fixed first. Blocks speaker notes.
2. **Coverage Gaps (HIGH PRIORITY)**: 3 critical code samples missing (T1078, T1110, T1565). Keaton flagged these in accuracy audit.
3. **Completeness (MEDIUM PRIORITY)**: 4 tactics underdeveloped (Reconnaissance, Resource Dev, C2, partial Lateral Movement). McManus quantified effort per slide.

**Dependencies Identified:**
- Task #1 (mapping clarity) must complete before Task #2 (speaker notes) — can't write notes without clear understanding
- Task #3 (code samples) unblocks Task #4–6 (tactic expansion) because samples provide reference implementations
- Task #7 (recap) can only happen after all 6 prior tasks complete

**Build Order Rationale:**
- Fix clarity first (1h) — highest ROI, unblocks multiple downstream tasks
- Add speaker notes next (6h) — critical path work; most effort; highest delivery impact
- Parallel code samples + tactic expansion (9h) — now unblocked by #1–2
- Recap + validation (3h) — can happen last; ties everything together

**Team Capacity Check:**
- McManus (Content): 12h available (Tasks #1, #2, #4, #5, #7) ✅
- Fenster (Research): 6h available (Tasks #3, #6) ✅
- Keaton (QA): spot-check at milestones ✅
- Chris (Owner): final signoff ✅

**Success Metrics:**
- 14/14 tactics covered (vs. 10/14 today)
- 85 slides total (vs. 71 today)
- 100% speaker notes (vs. 0% today)
- Keaton audit: A- → A
- PDF export verified
- Delivery-ready by EOD Day 3

**Document:** `.ai-team/decisions/inbox/kobayashi-build-order.md` (18KB)

**Status Update (2026-02-22 POST-MERGE):** Build order decision merged into `.ai-team/decisions.md`. This becomes the canonical execution plan for the 3-day sprint. All 7 tasks are now officially queued with clear ownership, dependencies, success criteria, and risk mitigation. Next action: Chris confirms team availability and Task #1 begins.

---

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

📌 Team update (2026-02-27): Always use 'claude-opus-4.6-1m' model for all agent spawns — decided by Chris Ayers (Copilot)
