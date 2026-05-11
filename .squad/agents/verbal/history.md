# Verbal — History

## Core Context

- **Project:** A Marp slide deck teaching developers the MITRE ATT&CK framework with code examples.
- **Role:** Marp Specialist
- **Joined:** 2026-05-11T15:55:39.701Z

## Learnings

<!-- Append learnings below -->

### 2026-05-11 — Techorama 2026 theme from .potx + DS Wallau

**Source template:** `/Users/chrisayers/Downloads/Techorama 2026 Template.potx`
**Display font:** DS Wallau (`DSWallau.ttf` + `DSWallauOsF.ttf`) from `/Users/chrisayers/Downloads/ds-wallau/`

**Extracted Color Palette (from `ppt/theme/theme1.xml`):**
| Token | Hex | Source |
|---|---|---|
| `--techo-navy`       | `#0E2841` | dk2 — primary dark background |
| `--techo-blue`       | `#156082` | accent1 — teal/steel blue |
| `--techo-orange`     | `#E97132` | accent2 — brand orange |
| `--techo-sky`        | `#0F9ED5` | accent4 — sky blue |
| `--techo-gold`       | `#E5C35A` | derived from sampling `content-bg.png` |
| `--techo-light-gray` | `#E8E8E8` | lt2 |
| `--techo-white`      | `#FFFFFF` | lt1 |

**File Locations Created:**
- Theme CSS: `slides/themes/custom-techorama.css`
- Fonts dir: `slides/themes/fonts/DSWallau.ttf`, `slides/themes/fonts/DSWallauOsF.ttf`
- Assets dir: `slides/themes/techorama/` (title-bg.png, content-bg.png, footer-strip.jpg, logo.png, title-graphic.png)
- Sample deck: `slides/techorama-sample.md`
- Preview HTML: `slides/techorama-preview.html` (Marp build verified ✅)

**Caveats:**
- DS Wallau font licensing: verify before commercial/public distribution.
- The .potx used `Aptos Display` (Microsoft 365 font) as its heading font — replaced with DS Wallau for the speaker-branding intent.
- `image13.png` (4.9 MB), `image16.jpg` (4.4 MB), `image17.jpg` (6.3 MB) were identified as large stock photos / placeholder content — not copied into the theme.
- `.emf` vector files (`image5.emf`, `image14.emf`) are not supported in CSS/HTML — omitted.
- The `.potx` slide color scheme is dark (navy bg) with warm gold/orange accents. White slides use these colors as heading/border accents.
### 2026-05-11 — Techorama theme validation recipe

- Validated Marp themes with two toolchains: Marp CLI (`html`, `pdf`, and `png`) plus Playwright against the served HTML preview.
- Caught path-resolution defects by checking PDF/PNG warnings and then confirming `document.fonts.check()` + computed styles in Playwright.
- Gotcha: Marp embeds theme CSS into output HTML, so local `url(...)` assets must resolve from the deck/output location used for preview; for slides in `slides/`, use `themes/...` paths. PNG export may need `--browser-timeout 90`.


### 2026-05-11 — Techorama applied to live MITRE ATT&CK deck

**Theme migration target:** `slides/Slides.md` from `custom-mitre-attack` to `custom-techorama`.

**Theme-coupled elements found:**
- Title slide used `![bg](./img/crooked-line-bg.svg)` plus scoped white/green heading CSS built for the prior light MITRE deck identity.
- No existing `_class` / `_color` directives were present; section divider slides were plain `# <!-- fit -->` slides.
- No inline `<span style="color:...">` assumptions and no Mermaid diagrams were present.
- Code-heavy slides used only scoped `pre` sizing, which remained compatible with the Techorama dark code block styling.

**Adaptations made:**
- Slide 1: removed the old crooked-line background image and scoped title colors, then applied `<!-- _class: title -->` so the Techorama navy patterned title background, DS Wallau headings, and gold accent render cleanly.
- Section divider slides: applied `<!-- _class: section -->` to the major transition slides so they use the Techorama navy/blue section treatment instead of default white content layout.
- Speaker notes: updated the title note so it no longer references a removed visual background.

**Validation notes:**
- HTML build passed.
- PDF build timed out at the default 30s but passed with `--browser-timeout 90`.
- PNG build passed and visual spot checks for title, agenda, code, and questions slides looked clean.
- Playwright confirmed `document.fonts.check('16px "DS Wallau"') === true`; only Font Awesome CDN font load failures and a favicon 404 appeared in console validation.

### 2026-05-11 — Enlarged Techorama section divider headings

**Feedback addressed:** Chris noted section headers like “Defense Evasion & Log Tampering” were too small.

**Finding:** The heading is on a `<!-- _class: section -->` divider slide and uses H1 with `<!-- fit -->`, so the governing selector is `section.section h1` in `slides/themes/custom-techorama.css`. Marp auto-scaling needed a larger width target in addition to a higher font-size ceiling; changing only `font-size` left the heading visually small.

**Theme update:**
- `section.section h1` font-size increased from `2.4em` to `18em` as the auto-scale ceiling.
- Added `width: 100%` and `max-width: 1100px` so fitted section titles can occupy the slide width.
- Added tighter `line-height: 0.95`, stronger `font-weight: 700`, thicker `border-bottom: 5px`, and reduced padding for a more dominant divider treatment.

**Validation:** Rebuilt `slides/Slides.html` and PNG outputs with `--theme-set slides/themes/custom-techorama.css`; Playwright spot-check screenshots were captured for slide 37 and slide 13 under `slides/validation-artifacts/post-fix/`.

### 2026-05-11 — Path A fix for section divider sizing

**Follow-up finding:** Marp `<!-- fit -->` injects auto-scaling behavior that overrides the intended CSS sizing on section divider H1s. The section flex layout also let the heading size against intrinsic content width, making CSS font-size bumps unreliable.

**Fix path chosen:** Path A — removed `<!-- fit -->` from all 10 `<!-- _class: section -->` divider headings in `slides/Slides.md` and made the section H1 CSS deterministic.

**Final section H1 treatment:** `section.section h1` uses `font-size: 4em`, `line-height: 1.02`, `font-weight: 700`, `width: 100%`, `max-width: 1120px`, and a `5px` gold underline. This produces consistent, dominant section headers while allowing long titles to wrap cleanly.

**Validation:** Rebuilt `slides/Slides.html` and all PNGs. Playwright confirmed section H1s no longer have `data-auto-scaling`; screenshot artifacts: `slides/validation-artifacts/post-fix/defense-evasion-section-path-a.png` and `slides/validation-artifacts/post-fix/think-like-attackers-section-path-a.png`.
