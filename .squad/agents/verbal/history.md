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

### 2026-05-11 — Current visual register for fantasy/medieval review

`slides/Slides.md` currently uses the `custom-techorama` theme: dark navy/blue section dividers, white content slides, DS Wallau display headings, gold/orange accents, and crisp corporate conference styling. Visuals are mostly technical diagrams, code samples, presenter/mascot imagery, and MITRE/security architecture graphics; fantasy additions should remain accent-level so they do not fight the SOC/red-team/developer-talk tone or reduce code/matrix readability.

### 2026-05-11 — Medieval accent layer applied to Techorama theme

**Theme hooks added:** appended `section.parchment`, `section.quest`, and `.battlement-rule` to `slides/themes/custom-techorama.css`.

**Design rationale:**
- `parchment` keeps the standard readable content-slide posture and adds only a warm gold/orange wash, inset gold frame, and heading accents for callouts or Defense in Depth.
- `quest` is a darker transition-slide treatment using the existing navy→blue Techorama gradient, DS Wallau display heading, gold underline, and a low-opacity castle-gate watermark.
- `.battlement-rule` is a tiny CSS-only crenellated divider utility for optional framing; it does not touch code block styling.

**Self-created SVG assets:** all are simple geometric silhouettes in `slides/themes/techorama/`, `viewBox="0 0 100 100"`, single-color via `currentColor`, no raster images or external font dependencies.
- `castle-gate.svg` — 309 bytes
- `tower.svg` — 238 bytes
- `shield.svg` — 253 bytes
- `scroll.svg` — 380 bytes

**Validation:** `slides/techorama-sample.md` was not present in this checkout, so the requested sample command could not produce an output file. Validated the same theme path with a minimal stdin Marp deck containing `quest`, `parchment`, and a code block; HTML render passed to `slides/validation-artifacts/techorama-medieval-check.html` with exit code 0.

### 2026-05-11 — POTX image extraction technique

- `.potx` files are ZIP archives; Office image assets can be copied directly from `ppt/media/` (and any other `*/media/` dirs such as `xl/media/`) without touching XML/layout/theme parts.
- Preserve canonical Office names (`image1.png`, etc.); watch for EMF/WMF vectors because Marp/HTML may need PNG/SVG conversion before use.

### 2026-05-11 — EMF→PNG conversion for Techorama assets

- Target assets: `slides/themes/techorama/image5.emf` (7.4 MB) and `slides/themes/techorama/image14.emf` (82 MB), extracted from the Techorama `.potx`.
- macOS conversion finding: LibreOffice headless and `libemf2svg`/`rsvg-convert` could open the EMFs but emitted blank white/transparent PNGs because the useful content was stored as EMF+ embedded bitmap records.
- Working path: extracted the embedded EMF+ bitmap payloads with Python/Pillow and wrote optimized PNGs.
- Final PNGs: `image5.png` — 1884×1023, 205 KB; `image14.png` — 4424×4822, 724 KB. `image14.png` stayed under 10 MB, so no downscaling was needed.
- Deleted the original `.emf` files after valid PNG output was confirmed with `file` and `magick identify`.

### 2026-05-12 — Techorama brand font wiring

- Alegreya Sans body fonts were bundled from the upstream Alegreya Sans GitHub TTF source after the Google Fonts ZIP endpoint returned non-ZIP content; the family is SIL OFL and only Light/Regular/Italic/Medium/Bold/BoldItalic are included to keep deck weight reasonable.
- Dreamhour is commercial and was not found locally, so the theme uses `local('Dreamhour')` with bundled SIL OFL UnifrakturMaguntia as the open-source blackletter fallback for logo/wordmark helpers.

### 2026-05-12 — POTX image rename cleanup

- Renamed 17 extracted `.potx` images from generic `image{N}.{png,jpg}` to descriptive kebab-case names based on visual content (e.g., `knight-on-horse-gray.png`, `techorama-logo-2026-medieval.png`, `robot-knight-mascot.png`, `brand-fonts-reference.png`).
- Prefixed Techorama-branded assets with `techorama-`; kept generic medieval artwork unprefixed for reuse flexibility.
- Pre-existing tracked files (`logo.png`, `title-bg.png`, `content-bg.png`, `footer-strip.jpg`, `title-graphic.png`, SVGs) were untouched.

### 2026-05-12 — Redundant table cleanup pattern

**Pattern:** When an image already contains a visual data table (e.g., a 3×3 alignment chart grid), do not duplicate the same table as parallel text content on the slide.

**Fix applied:** Removed the text-format 3×3 alignment table from the "Deployment Security Alignment Chart" meme slide. The image `alignment-chart.jpg` (1200×900) already renders the Lawful/Neutral/Chaotic × Good/Neutral/Evil grid baked into the visual. Duplicating this as a Markdown table on the right side of the `<div class="columns">` layout created visual clutter and caused cutoff issues.

**Result:** Single-column slide with centered image at `![h:540 center]`, title above, ATT&CK lens caption below. Marp validation: exit code 0. Slide count: 79 (unchanged). Image fits cleanly within 1280×720 bounds without cutoff.

**Lesson for future slides:** If an image is the primary teaching content and contains detailed data/text, let it dominate the slide without parallel text tables. Reserve slide real estate for callouts, captions, or speaker notes instead.

### 2026-05-12 — PIL image regeneration for clipped meme fix

**Problem:** `slides/img/memes/alignment-chart.jpg` had left-margin clipping — the "N" in "NEUTRAL" row header was cut off at the pixel level.

**Fix approach:**
1. Sample bg/text colors from the broken source using PIL `getpixel()` before overwriting.
2. Regenerate the entire image from scratch with PIL, using adequate left margin (140px) for row labels.
3. Save generation script to `slides/themes/scripts/generate-alignment-chart.py` for future maintenance.

**Sampled colors:** Background RGB(248,242,222), Text/Border RGB(40,28,13).
**Fonts used:** Impact (`/System/Library/Fonts/Supplemental/Impact.ttf`) for bold, Helvetica (`/System/Library/Fonts/Helvetica.ttc`) for body.
**Final layout:** 1200×900 canvas, 140px left margin, 346×246px cells, 3px borders.

**Reusable pattern:** For any clipped-label meme image, sample colors from the source, then regenerate via PIL with proper margins rather than attempting pixel-level repairs.

### 2026-05-12 — Alignment chart re-rendered with Techorama brand fonts

**Task:** Replace Impact + Helvetica system fonts in `slides/img/memes/alignment-chart.jpg` with bundled Techorama brand fonts.

**Font mapping applied:**
- **Internal title & column/row headers:** Alegreya Sans Bold (30pt for headers, 42pt for title)
- **Cell role names:** Alegreya Sans Bold (30pt, all caps)
- **Cell taglines:** Alegreya Sans Italic (18pt, lowercase for supporting text feel)

**Script location:** `slides/themes/scripts/generate-alignment-chart.py` (updated to load TTFs from `slides/themes/fonts/`)

**Finding:** Alegreya Sans is more open/spacious than Impact, so point sizes were reduced slightly (42→38 for title had spacing room; headers/roles stayed at 30pt with good legibility). No text overflow occurred in the 1200×900 canvas with 140px left margin. NEUTRAL row label renders fully.

**Verification:** All 9 cells readable, title fits, "NEUTRAL" row label fully visible, cell taglines don't overflow.

**Reusable pattern:** For PIL-generated meme images, always use bundled TTF fonts from `slides/themes/fonts/` rather than system fonts. Specify point sizes conservatively and test overflow before deployment.
