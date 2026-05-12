# Verbal — History

## Core Context

- **Project:** A Marp slide deck teaching developers the MITRE ATT&CK framework with code examples.
- **Role:** Marp Specialist
- **Joined:** 2026-05-11T15:55:39.701Z

## Key Expertise Developed

### Techorama 2026 Theme Implementation
- Extracted color palette and DS Wallau display fonts from .potx template (navy `#0E2841`, blue `#156082`, orange `#E97132`, gold `#E5C35A`)
- Created `custom-techorama.css` with section/parchment/quest classes and self-created SVG assets (castle-gate, tower, shield, scroll)
- Applied theme to live `slides/Slides.md` with `<!-- _class: title -->` and `<!-- _class: section -->` markup
- Established section H1 sizing (4em font-size, 1.02 line-height, 5px gold underline) without `<!-- fit -->` for consistent header dominance

### Validation Toolchain
- Docker `marpteam/marp-cli:latest` on Windows with `--browser-timeout 120` for PNG/PDF builds on 77+ slide decks
- Playwright HTML preview via bespoke.js navigation with `querySelectorAll('svg.bespoke-marp-slide')`
- Screenshot via `clip: { x: 0, y: 0, width: 1280, height: 720 }` for exact slide crop
- Font verification: `document.fonts.check()` for DS Wallau and Alegreya Sans loaded state

### Image Asset Management
- EMF→PNG conversion: extracted EMF+ embedded bitmaps via Python/Pillow (not LibreOffice/rsvg, which emitted blanks)
- Renamed 17 extracted images to kebab-case (e.g., `knight-on-horse-gray.png`, `techorama-hero-medieval.png`)
- Bundled Alegreya Sans (SIL OFL, 6 weights) + UnifrakturMaguntia (blackletter fallback) in `slides/themes/fonts/`
- PIL image regeneration for meme clipping fixes: sampled colors then recreated from scratch with proper margins
- Reusable pattern for `![bg]` assets: full-bleed landscape JPEG/PNG (no alpha); portrait RGBA creates incomplete coverage

### Canonical Opacity Locking (2026-05-12)
- Discovered three opacity-modifier regressions when Marp `![bg opacity:X]` syntax dropped opacity modifiers or used wrong assets
- Created canonical opacity reference table in decisions.md locked against future regression
- Applied 4 targeted corrections: lines 238 (Initial Access `.2`), 475 (Persistence `.2`), 824 (Supply Chain `.2`), 1047 (Collection `.2`)
- Swapped Defense Evasion from `hero-torches.png` (portrait, 45% transparent padding) to `stone-wall-texture-dark.jpg` for complete coverage

### Reviewer Lockout Protocol (First Invocation)
- Assigned revision authority after Keyser produced two consecutive identical opacity regressions despite documentation
- Executed targeted fix on lines 582/724, re-validated all section dividers (8/8 pass)
- Lock-down mechanism: canonical table in decisions.md + team notices to mcmanus/fenster on precedent

## Learnings Condensed

- **Marp path resolution:** Relative URLs in `@font-face` resolve from HTML file location; serve from `slides/` if assets there
- **Docker on Windows:** `\D:\mitre-attack-for-devs` resolves correctly in PowerShell volume mounts; use `--browser-timeout 120` for 77+ slides
- **Playwright-cli side effects:** `install --skills` modifies `.claude/skills/` (tracked, not artifacts) — document/skip on validation runs
- **Benign warning:** Marp scans code blocks for file paths; `./sbom.json` in fenced code triggers false-positive (no visual impact)
- **Opacity table design:** Stone `.15`/`.2` for grain, silhouettes `.2` for visibility, hero images `.2`–`.25`, Celtic accent `.08`
- **PIL image regeneration:** Sample colors from source, regenerate with adequate margins; always use bundled TTF fonts from `slides/themes/fonts/`
- **Alignment chart:** Alegreya Sans more open than Impact; reduce point sizes and test overflow in 1200×900 canvas with 140px left margin

## Session 2026-05-12 Outcome

- Final validation: HTML ✅, PDF ✅, PNG 77/77 ✅
- All section dividers legible and visually coherent
- Canonical opacity table locked; Reviewer Lockout precedent established
- Deck ready for Chris to commit; `.squad/agents/verbal/history.md` updated with learnings
