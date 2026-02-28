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

### MITRE Overview Slides Addition (2026-02-28)

- **Slide Insertion Pattern**: New contextual slides inserted between existing conceptual slides (OWASP → MITRE org → MITRE ecosystem → Why devs care → ATT&CK specifically). This progressive disclosure pattern — organization → ecosystem → relevance → specific framework — works well for audiences unfamiliar with MITRE beyond ATT&CK.

- **Mermaid Diagram for Framework Relationships**: Used a top-down flowchart with relationship labels between MITRE frameworks (CVE, CWE, CAPEC, ATT&CK, D3FEND, ATLAS). Color-coded by category: red accent for ATT&CK (primary focus), green for defensive (D3FEND), orange for vulnerability/weakness (CVE/CWE), purple for emerging (ATLAS). Dark backgrounds match custom-default theme aesthetic.

- **Speaker Note Depth Calibration for Context Slides**: For organizational/ecosystem overview slides, speaker notes should provide historical context, analogies to things developers already use (Dependabot → CVE, Snyk → CWE), and explicit "why should you care" framing. These bridge slides need more persuasion than technical slides.

- **Slide Count Impact**: Three new slides added (lines 81–137 in Slides.md). Total deck now approximately 74+ slides. At ~1 minute per context slide, adds roughly 3 minutes to delivery time — well within buffer for a 60-75 minute presentation.

### CVE, Attack Chains, and Crooked Line Slides (2026-02-28)

- **Insertion Point Pattern**: New concept slides inserted between "The 14 ATT&CK Tactics" diagram and "OWASP vs ATT&CK" comparison. This placement builds progressively: taxonomy → individual techniques → CVE relationship → chained attacks → non-linear reality → comparison. Each slide deepens the audience's mental model before moving to the next abstraction layer.

- **Attack Chain Diagram Convention**: Used color-coded Mermaid flowcharts for attack chains with a gradient from red (initial access) through orange/yellow (mid-chain) to purple/dark (exfiltration/impact). This visual progression reinforces the temporal flow of an attack. Two chain examples shown: supply chain and file upload to ransomware — sourced from Fenster's attack-research.md chains 1 and 4.

- **Crooked Line Visualization**: The looping-back arrows in Mermaid (`D --> C`, `E --> C`) with `linkStyle` highlighting in red (#e94560) effectively show the non-linear nature of real attacks. This is the "aha moment" slide — contrasts with the linear kill chain using a two-column layout for direct comparison before showing the diagram.

- **CVE-to-ATT&CK Bridge**: Log4Shell (CVE-2021-44228) used as the canonical example of one CVE enabling multiple ATT&CK techniques (T1190, T1059, T1105). This example resonates with developers because most remember the Log4Shell incident. Speaker notes emphasize the "patch vs. detect" distinction — CVEs tell you what to fix, ATT&CK tells you what to watch for.

- **Slide Count Impact**: Five new slides added. Total deck now approximately 79+ slides. At ~1-2 minutes per concept slide (more for diagram discussion), adds roughly 7-10 minutes. The crooked line slides in particular invite audience discussion and should be paced accordingly.

- **Mermaid Color Palette Convention**: Established consistent color assignments across attack chain diagrams: red (#e74c3c) for initial access/exploit, orange (#e67e22) for execution, yellow (#f39c12) for credential-related, green (#2ecc71) for movement/access, blue (#3498db) for discovery, purple (#9b59b6) for collection/manipulation, dark (#1a1a2e) for final impact. Matches custom-default theme aesthetic.

📌 Team update (2026-02-27): Always use 'claude-opus-4.6-1m' model for all agent spawns — decided by Chris Ayers (Copilot)

### Kobayashi Review Fixes (2026-02-28)

- **Duplicate Content Detection**: User enumeration (login "User not found" vs "Wrong password") was taught identically in both Discovery (T1087) and Reconnaissance (T1589) sections. When the same vulnerability pattern appears in multiple tactics, each section must use a *distinct example* to justify its existence. Discovery kept the login example; Reconnaissance was rewritten to use password reset form enumeration — a different but equally important T1589 vector.

- **Summary Table Must Match Content**: The "What We Covered" recap table omitted Supply Chain despite a full 6-slide section covering T1195/T1195.001 with attack examples, CLI tools, integrity validation code, and a Mermaid flow diagram. Speaker notes compounded the error by claiming Supply Chain *wasn't* covered. Lesson: always rebuild summary tables from the actual slide structure, never from memory.

- **Technique ID Precision**: T1059.006 (Python) was listed in the summary but no slide specifically teaches Python command injection — the Execution section uses C# for command injection and Python for deserialization (T1203). Changed to T1059 (general) + T1203 to match actual content. Always verify sub-technique references against the slides that teach them.

- **Official ATT&CK Names Matter**: T1046 was labeled "Network Service Scanning" — the correct name is "Network Service Discovery." Always cross-reference technique names with attack.mitre.org. Audiences familiar with ATT&CK will notice incorrect names immediately.

- **Placeholder Slides Are Liabilities**: A bare "# DEMOS" slide with a vague speaker note adds nothing. Converted to a "Live Demo" transition slide with specific demo scenarios (SQL injection, credential stuffing, web shell upload) and a graceful skip path. Every slide must earn its place in the deck.

### Fenster Technique ID Corrections (2025-07-17)

- **T1185 vs T1539 Distinction**: T1185 (Browser Session Hijacking) describes man-in-the-browser attacks — adversary malware injecting into a browser process to pivot through authenticated sessions. T1539 (Steal Web Session Cookie) describes cookie theft and replay — XSS-based exfiltration, insecure cookie flags, session fixation. Our session management slides teach cookie security, not browser process injection, so T1539 is the correct mapping. Applied 16 replacements across slide content, code comments, speaker notes, and summary tables.

- **SSRF ATT&CK Mapping Precision**: SSRF was mapped to T1090 (Proxy) + T1572 (Protocol Tunneling) — both are C2 evasion techniques. The correct mapping is T1190 (Exploit Public-Facing Application) because SSRF is an application exploitation technique. ATT&CK mapping should reflect what the adversary *does* (exploits a public-facing app), not the incidental mechanic (server acts as proxy). Changed in the OWASP-to-ATT&CK mapping table.

- **Cross-Reference Technique IDs Against Framework**: When assigning ATT&CK technique IDs, always verify against attack.mitre.org. Conceptual similarity ("session hijacking" sounds like it should be T1185) can lead to incorrect mappings. The technique description, not the name, determines the correct ID.
