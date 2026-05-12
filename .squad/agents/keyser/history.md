# Keyser — History

## Core Context

- **Project:** A Marp slide deck teaching developers the MITRE ATT&CK framework with code examples.
- **Role:** Lead
- **Joined:** 2026-05-11T15:55:39.698Z

## Learnings

- **2026-05-11 — Team update:** Three-agent sprint completed on MITRE ATT&CK deck. mcmanus (gpt-5.5) delivered supply-chain case-study research (Shai-Hulud, Notepad++ Chrysalis, Axios verified, bonus roster) and three key decisions: acronym expansion convention, medieval motif confinement (section intros only, no code rewrites), and supply-chain narrative arc (event-stream → modern npm worm → developer tool hijack → enterprise compromise). verbal applied Techorama theme to `slides/Slides.md` with fantasy accent layer proposal. If resuming research or content work, these decisions are now in `decisions.md` and ready for implementation.

- **2026-05-12 — Deck compaction framework:** For future deck reviews, use 3-dimension slide scoring (pacing value, content payload, cut cost — each high/med/low) plus detection patterns: double-ceremony section dividers (`# X` followed by `## X` content), meme inflation audit (rank all memes, cut the bottom third for 45-min talks), case-study glut (consolidate similar cases or cut the "everyone knows this" entry), vulnerable/defended code pair compression (side-by-side diff vs two-slide reveal), and section-intro table consolidation. Output a tiered proposal (A: strong cuts, B: compression, C: keep) with clear rationale before any executor agent touches the deck.

- **2026-05-12 — Section divider image patterns:** When adding Techorama/medieval background images to Marp `section`-class slides: (a) use `![bg right:30% fit]` for silhouette/figure assets (knight, portrait) so the title text has clear left space; (b) use `![bg opacity:.15–.25]` for full-frame textures and hero scenes — busier patterns need lower opacity (0.15–0.20), simpler hero images can go to 0.25; (c) skip images on sections that immediately precede code-heavy slides if there is no per-slide bg override — bg images bleed through on following slides; (d) closing/feedback slides suit a brand wordmark (PNG preferred) rather than atmospheric imagery.

- **2026-05-12 — Acronym shift risk:** After content additions to a Marp deck (new slides inserted mid-file), verify first-visible-content acronym expansions. Line numbers in applied-decision notes drift as the file grows; always grep for the bare acronym in visible content rather than trusting the recorded line number.
