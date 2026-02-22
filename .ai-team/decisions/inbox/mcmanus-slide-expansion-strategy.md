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
