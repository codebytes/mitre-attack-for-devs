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

---

### 2026-02-27: Full Deck Review — 101 Slides, Structural Issues Identified

**Deck State:** slides/Slides.md is now ~2207 lines, ~101 slides covering 13 of 14 ATT&CK tactics.

**Key Structural Finding:** User enumeration vulnerability (login returning different errors for "user not found" vs "wrong password") is taught twice:
- Discovery section (T1087, lines 1148-1195): vulnerable + defended login code
- Reconnaissance section (T1589, lines 1719-1779): nearly identical vulnerable + defended login code
These must be consolidated. Keep one, cross-reference the other.

**Agenda Inconsistency:** Slide says "11 Technique Categories" but deck now covers 13 tactics. Speaker note references "11 tactic categories." Must update to reflect actual content.

**"What We Covered" Table Error:** Table on line 2080 omits Supply Chain entirely, and speaker note claims "The only tactic we didn't deep-dive is Supply Chain" — but Supply Chain has a full 6-slide section (lines 1235-1352). Table needs a 14th row for Supply Chain; speaker note needs correction.

**T1059.006 Reference:** "What We Covered" table lists T1059.006 (Python) under Execution, but slides only demonstrate T1059 generally. Either add Python-specific content or remove the sub-technique reference.

**Technique ID Flag for Fenster:** T1185 (Browser Session Hijacking) used in Persistence section for session cookie theft — in modern ATT&CK, T1185 specifically describes man-in-the-browser attacks; session cookie theft is T1539 (Steal Web Session Cookie). Needs Fenster verification.

**T1046 Naming:** Listed as "Network Service Scanning" but official ATT&CK name is "Network Service Discovery."

**Section Balance:**
- Strong (5-6 slides): Initial Access, Execution, Persistence, Priv Esc, Cred Access, Supply Chain, Collection/Exfil, Impact
- Thin (2-3 slides): Lateral Movement, Reconnaissance, Resource Development, C2
- Resource Dev and C2 only show defended code, no vulnerable-defended pairs

**Front-loading:** 19 slides before "Let's Think Like Attackers" transition. Heavy but mitigated by Mermaid diagrams. Acceptable.

**Overall Rating:** 4/5 — strong deck, excellent code samples, solid speaker notes. Fix the redundancy, correct the summary table, and verify T1185.

---

### 2026-02-28: Deck Review Issues — All Resolved

**Resolution Status:** All 7 issues from 2026-02-27 review have been resolved:

1. ✅ **User Enumeration Redundancy** — McManus consolidated: kept detailed version in Discovery (T1087), replaced Reconnaissance example with distinct T1589 pattern (password reset enumeration) with cross-reference.

2. ✅ **"What We Covered" Table** — Added Supply Chain row (`T1195, T1195.001 | Dependency verification, integrity validation`). Updated speaker note from "The only tactic we didn't deep-dive is Supply Chain" to "all 14 tactics."

3. ✅ **Agenda Count** — Updated line 44 from "11 Technique Categories" to "13 Tactic Categories." Updated speaker note.

4. ✅ **T1046 Name** — Corrected from "Network Service Scanning" to "Network Service Discovery."

5. ✅ **DEMOS Placeholder** — Replaced with proper transition slide.

6. ✅ **T1185 → T1539 (Fenster verified)** — Confirmed change needed. T1185 = browser process injection; T1539 = cookie theft. Applied 16 corrections across content, code comments, and summary tables.

7. ✅ **SSRF T1090/T1572 → T1190 (Fenster verified)** — Confirmed change needed. SSRF is application exploitation (T1190), not C2 evasion. Applied 1 correction to OWASP mapping table.

**Session Log:** `.ai-team/log/2026-02-28-deck-review-fixes.md`

**Decisions Merged:** Full Deck Review findings + Attack Chain Color Standards consolidated into `.ai-team/decisions.md`.
