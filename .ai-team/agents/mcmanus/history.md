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
