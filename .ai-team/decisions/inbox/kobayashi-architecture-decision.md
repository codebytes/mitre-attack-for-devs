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
