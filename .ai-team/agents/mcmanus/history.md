# Project Context

- **Owner:** Chris Ayers (clayers@gmail.com)
- **Project:** MITRE ATT&CK for Developers — deep-dive research into ATT&CK framework, Marp slide decks, and multi-language code samples (Python, .NET, JavaScript) showing attack techniques and defenses
- **Stack:** Marp (Markdown slides), Python, .NET/C#, JavaScript, Mermaid diagrams
- **Created:** 2026-02-22

## Learnings

### Deep-Dive Slide Deck Analysis (2026-02-22)

- **Slide Structure Convention**: ATT&CK presentations use a "Technique Overview → Vulnerable Code → Defended Code" repeating pattern across tactics. This is intuitive for audiences and teaches cause-and-effect.

- **Marp Conventions in This Project**:
  - Custom theme: `custom-default.css` (also have `custom-gaia.css`, `custom-uncover.css`)
  - Section breaks use `# <!-- fit -->` for full-width headers
  - Multi-language code examples are acceptable when language-tagged consistently
  - Mermaid diagrams embedded as `<div class="mermaid">` blocks with script tag at end of file
  - Two-column layouts use `<div class="columns">` and three-column use `<div class="columns3">`
  - Global footer via frontmatter; individual slide footers via `<!-- _footer: '...' -->`

- **Critical Gap**: Speaker notes are absent from the deck. For a ~75-minute deep-dive presentation, speaker notes are non-negotiable. They provide delivery confidence, talking points, pacing guidance, and enable other presenters to deliver the same content.

- **Tactic Coverage Insight**: 10 of 14 ATT&CK tactics are substantially covered. The 4 gaps (Reconnaissance, Resource Development, Command & Control, and partial Lateral Movement) represent about 5–10% of typical developer responsibility but are important for completeness and threat modeling context.

- **Code Example Quality**: The deck's strength is in multi-language (Python, C#, JavaScript) authentic, runnable code examples. Each technique is paired with vulnerable AND defended versions. This "before/after" pattern is highly effective for teaching secure design patterns.

- **Closure Problem**: The deck ends at slide 71 (Questions?) without a recap of what was covered, what wasn't, or explicit next steps. For long-form presentations, recap + roadmap slides significantly improve retention and action items.

- **Delivery Timing**: At 71 slides with 28+ code examples and 7 Mermaid diagrams, this is a 60–75 minute presentation if well-paced. Speaker notes help manage pacing.

### Speaker Notes Addition (2026-02-22)

- **Speaker Note Conventions Established**: Speaker notes use HTML comment syntax (`<!-- -->`) placed after slide content but before the `---` separator. Each note provides 2-5 sentences covering key talking points, transitions, real-world context, timing guidance, and audience engagement prompts.

- **Note Content Strategy**: For code slides, notes explain what to highlight and walk through. For diagram slides, notes describe the narrative flow. For section headers, notes set up what's coming. For concept slides, notes provide analogies and context. For closing slides, notes include wrap-up talking points and calls to action.

- **Presenter Guidance Patterns**: Notes include explicit timing cues ("Spend 2-3 minutes here"), transition phrases ("This leads us to...", "Building on that..."), audience engagement prompts ("Ask the audience...", "Show of hands..."), and emphasis markers for critical concepts that need reinforcement.

- **Technical Depth Calibration**: Speaker notes translate dense technical concepts into presenter-friendly language, providing analogies and real-world examples to illustrate abstract ATT&CK techniques. This helps presenters who understand security but may not have memorized every technique ID and name.

- **Comprehensive Coverage**: Added speaker notes to all 71+ slides including title slide, bio, agenda, concept explanations, code examples (both vulnerable and defended), diagrams, section transitions, implementation guidance, resources, and closing Q&A. Every slide now has delivery guidance.

## Team Decisions Affecting This Agent

**Speaker Note Conventions Decision (2026-02-22):** Merged from decisions inbox into `.ai-team/decisions.md`. This decision establishes team standards for all future presentations and ensures consistent delivery across multiple speakers. Key impact: enables rapid onboarding of new presenters and ensures messaging consistency across venues.
