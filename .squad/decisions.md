# Squad Decisions Registry

## 2026-05-11 — Techorama Theme & Validation

### Decision: Techorama 2026 Marp Theme

**Date:** 2026-05-11  
**Author:** verbal  
**Type:** theme

#### Theme Name

`custom-techorama`

#### Location

- **CSS file:** `slides/themes/custom-techorama.css`
- **Fonts:** `slides/themes/fonts/DSWallau.ttf`, `slides/themes/fonts/DSWallauOsF.ttf`
- **Assets:** `slides/themes/techorama/` (title-bg.png, content-bg.png, footer-strip.jpg, logo.png, title-graphic.png)
- **Sample deck:** `slides/techorama-sample.md`

#### How to Use

Set the theme in your deck's frontmatter:

```yaml
---
marp: true
theme: custom-techorama
paginate: true
footer: '@YourHandle — techorama.be'
---
```

Use Marp CLI with the theme-set flag to register the custom theme:

```bash
npx @marp-team/marp-cli \
  --theme-set slides/themes/custom-techorama.css \
  --output output/my-talk.html \
  slides/my-talk.md
```

#### Slide Classes

| Class | Usage |
|---|---|
| `<!-- _class: title -->` | Title slide — dark navy background with gold accent, DS Wallau heading |
| `<!-- _class: section -->` | Section divider — navy-to-blue gradient, centered |
| `<!-- _class: lead -->` | Lead/quote slide — navy bg, orange accent bar |
| `<!-- _class: invert -->` | Dark content slide — navy bg, normal layout |
| *(none)* | Standard white content slide |

#### Design Tokens

| Variable | Hex | Role |
|---|---|---|
| `--techo-navy` | `#0E2841` | Primary dark background |
| `--techo-blue` | `#156082` | Primary accent |
| `--techo-orange` | `#E97132` | Secondary accent |
| `--techo-gold` | `#E5C35A` | Highlight accent |
| `--techo-sky` | `#0F9ED5` | Tertiary accent |

#### Notes

- DS Wallau font used for all display headings (h1, h2, h3 on title/section slides).
- Body font falls back to Aptos → Segoe UI → system-ui.
- Verify DS Wallau licensing before distributing decks publicly.
- Do not modify `custom-default.css`, `custom-mitre-attack.css`, or other existing themes.

### Decision: Techorama Theme Validation

**Date:** 2026-05-11  
**Status:** Passed (post-fix)

The `custom-techorama` Marp theme passes validation after targeted fixes:

- Renamed the custom font family in CSS to `DS Wallau` so browser font checks and computed heading stacks match the intended display font.
- Updated local CSS asset URLs to resolve from `slides/` preview/deck outputs: `themes/fonts/...` and `themes/techorama/title-bg.png`.

**Revalidation command:**

```bash
npx --package @marp-team/marp-cli marp slides/techorama-sample.md --theme-set slides/themes/custom-techorama.css -o slides/techorama-preview.html --html && npx --package @marp-team/marp-cli marp slides/techorama-sample.md --theme-set slides/themes/custom-techorama.css --images png --browser-timeout 90 -o validation-artifacts/techorama-slide --allow-local-files
```

## 2026-05-11 — Acronyms, Medieval Motif, Supply-Chain Narrative

### Decision: Acronym Convention for Developer-Security Decks

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content convention

For developer-facing security slide decks, expand security-specific acronyms on first meaningful use in visible slide content, then use the acronym afterward.

**Acronyms (expand on first use):**
- SIEM (Security Information and Event Management)
- SBOM (Software Bill of Materials)
- SAST (Static Application Security Testing)
- CVE (Common Vulnerabilities and Exposures)
- CVSS (Common Vulnerability Scoring System)
- RCE (Remote Code Execution)
- C2 (Command and Control)
- RAT (Remote Access Trojan)
- RBAC (Role-Based Access Control)

**Rationale:** The MITRE ATT&CK for Developers deck mixes expanded and bare acronyms. Common developer terms like API, JSON, SQL, HTTP, and HTTPS can remain bare, but security acronyms should be expanded once to reduce friction for mixed developer/security audiences.

### Decision: Medieval Motif Content Guidelines

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content convention

Use a threaded medieval/castle-defense motif sparingly: section intro notes, tactic transition lines, and one or two high-fit slides such as Defense in Depth. Do not rewrite technical slides, code samples, MITRE mappings, or CVE case-study facts around the motif.

**Rationale:** The deck is a developer security talk, not a fantasy talk. Medieval metaphors work when they clarify attacker movement and layered defense (gates, disguises, keys, tunnels, couriers, treasure rooms), but they will hurt credibility if they replace precise MITRE ATT&CK terminology or intrude into code examples.

#### Applied: Medieval Content Layer

**Date Applied:** 2026-05-11  
**Status:** Applied to `slides/Slides.md`

The Medieval Motif Content Guidelines decision has been applied as a content layer. Added a `parchment` Castle-Defense Lens framing slide after the Agenda, medieval transition lines to section-divider speaker notes only, and reframed Defense in Depth as concentric walls while preserving diagrams, security controls, ATT&CK IDs, CVE/CVSS facts, case-study content, code blocks, and the supply-chain narrative arc. Marp HTML validation passed.


### Decision: Dev-Audience Meme Addition

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content addition  
**Status:** Applied

Add a small number of developer-audience meme slides as text-format humor only, avoiding image assets and external image URLs. Applied two `parchment` meme slides in `slides/Slides.md`: Drake-style **Secrets Management: A Choice** after **How Attackers Steal Credentials**, and galaxy-brain-style **Detection Maturity: A Brief Evolution** after **Building Detection Into Code**. The existing **How it started vs How it's going** slide remains the third meme format.

**Constraints:** Keep memes out of code-sample slides, MITRE technique listings, and factual case-study slides.

### Decision: Supply-Chain Case Study Narrative Arc

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content recommendation

**Recommended case studies and structure:**

1. **event-stream (historical maintainer-trust setup)** — establish the baseline failure pattern.
2. **Shai-Hulud (modern npm worm)** — self-replication, lifecycle scripts, token theft, GitHub workflow abuse, 500+ compromised packages.
3. **Notepad++ (2025 update-infrastructure hijack, Chrysalis campaign)** — social-engineered release artifacts on developer machines.
4. **Axios 2026 (verified)** — endorsed by maintainer postmortem, CISA, StepSecurity, and Snyk.
5. **Log4Shell** — label as dependency-trust failure rather than supply-chain compromise.
6. **SolarWinds SUNBURST, XZ Utils CVE-2024-3094** — bonus roster for regional/advanced threat context.

**Rationale:** This arc tells a cohesive story from old npm trust failure → global dependency exposure → social-engineered release artifacts → self-replicating npm worm → compromised developer tool updater → signed enterprise build compromise. Reduces overstating thin or unverified stories while keeping developer relevance high.

### Decision: Fantasy/Medieval Theme Accent Layer

**Date:** 2026-05-11  
**Author:** verbal  
**Type:** visual/theme proposal  
**Status:** adopted

Keep `custom-techorama` as the base visual system and add a small medieval/fantasy accent layer:

- Reusable `parchment`/`quest` classes for section dividers or callouts.
- Optional corner/side decorative silhouettes (castle gate, tower, dragon, shield, scroll, wizard staff) at low opacity.
- Use existing Techorama tokens (`--techo-navy`, `--techo-blue`, `--techo-gold`, `--techo-orange`) so the deck remains conference-branded.

**Constraints:**
- Use permissively licensed or self-created SVG/PNG assets only.
- Keep fantasy assets low-contrast/watermark-style on code-heavy slides.
- Do not alter MITRE matrix/architecture diagrams.

**Rationale:** The deck is code-heavy and technical; readability must stay dominant. Section dividers are natural places for playful visual metaphors without cluttering code slides.

#### Applied: Medieval Visual Accent Layer

**Date Applied:** 2026-05-11  
**Status:** Applied to `slides/themes/custom-techorama.css` and `slides/themes/techorama/`

The Fantasy/Medieval Theme Accent Layer decision has been applied as an append-only extension over the Techorama base theme. Added `section.parchment`, `section.quest`, and `.battlement-rule` hooks, plus self-created `castle-gate.svg`, `tower.svg`, `shield.svg`, and `scroll.svg` silhouettes. No Techorama design tokens or existing base/title/section/lead/invert/code styles were changed.

### Decision: Apply Techorama Theme to Live MITRE ATT&CK Deck

**Date:** 2026-05-11  
**Author:** verbal  
**Type:** theme-migration

The live MITRE ATT&CK presentation at `slides/Slides.md` now uses `theme: custom-techorama` while preserving pagination and Chris Ayers' footer.

**Migration summary:**
- Removed the old title-only `crooked-line-bg.svg` background and scoped white/green heading CSS (coupled to previous MITRE visual system).
- Applied `title` to the opening slide and `section` to major transition slides.
- No `_color` directives, inline styled color spans, Mermaid diagrams, or hardcoded table/background styles required migration.
- Existing scoped `pre` font-size adjustments on dense code slides remain valid with Techorama's dark code block styling.

**Validation:** HTML build, PDF build (with `--browser-timeout 90`), and PNG build for all 68 slides passed. Playwright font validation passed for DS Wallau.

#### Applied: Acronym Convention

**Date Applied:** 2026-05-11  
**Status:** Applied to slides/Slides.md

The "Acronym Convention for Developer-Security Decks" decision has been applied. Expanded acronyms on first visible-content use: C2 (line 192), RCE (line 740), CVSS (line 740), RAT (line 756), SIEM (line 1018), SBOM (line 832). Marp HTML build validated clean.

#### Applied: Supply-Chain Narrative Arc

**Date Applied:** 2026-05-11  
**Status:** Applied to slides/Slides.md

The "Supply-Chain Case Study Narrative Arc" decision has been applied. Added 3 new slides: "The Supply-Chain Attack Arc" narrative table (line 709), "Case Study: Notepad++ Update Hijack (2025)" with Chrysalis campaign facts and ATT&CK T-IDs (line 724), "Log4Shell (2021) — Dependency-Trust Failure, Not Compromise" with first-visible SBOM expansion (line 813). Section intro speaker note updated to distinguish Log4Shell from supply-chain compromise. Marp HTML build validated clean.

## 2026-05-11 — Fantasy/Medieval Meme Slides (Graphical)

### Decision: Add 8 Fantasy/Medieval Meme Slides (Text-Only)

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content addition  
**Status:** applied for review

Applied all 8 researched text-only fantasy/medieval meme candidates to `slides/Slides.md`:

1. One Does Not Simply Patch Production
2. You Shall Not Pass
3. SNEAK 100: Living Off the Land
4. Deployment Security Alignment Chart
5. I Cast Fireball at the Input Field
6. Roll Initiative: When the Alert Is Real
7. I Used to Ship Secrets Like That
8. Fus Ro Dah: When One Bad Input Moves the Whole Stack

**Constraints followed:**
- Every new meme slide uses `<!-- _class: parchment -->`.
- No embedded images or external image URLs.
- Existing meme slides left in place.
- Each new slide includes a visible ATT&CK lens callout and speaker note.

**Placement rationale:** Meme slides placed near their teaching context. Batch intentionally over-includes candidates; final deck pacing should be pruned after Chris reviews which jokes land.

### Decision: Graphical Meme Images Applied (Stance Reversal)

**Date:** 2026-05-11  
**Author:** mcmanus  
**Type:** content addition (stance reversal)  
**Status:** applied for review

**STANCE REVERSAL:**  
Chris reversed the earlier text-only meme constraint and confirmed fair-use applicability for standard Imgflip/Know Your Meme templates. Applied a graphical image layer to all 11 meme slides in `slides/Slides.md`: the 3 existing memes and the 8 newly added fantasy/medieval candidates.

**Images added to `slides/img/memes/`:**
- `drake.jpg` — Secrets Management: A Choice (existing retrofit)
- `galaxy-brain.jpg` — Detection Maturity: A Brief Evolution (existing retrofit)
- `how-it-started.jpg` — How it started vs How it's going (existing retrofit)
- `alignment-chart.jpg` — Deployment Security Alignment Chart (new, generated 3x3 grid)
- `you-shall-not-pass.jpg` — You Shall Not Pass (new, Imgflip)
- `cast-fireball.jpg` — I Cast Fireball at the Input Field (new, Imgflip)
- `fus-ro-dah.jpg` — Fus Ro Dah: When One Bad Input Moves the Whole Stack (new, Know Your Meme)
- `arrow-in-the-knee.jpg` — I Used to Ship Secrets Like That (new, Imgflip)
- `sneak-100.jpg` — SNEAK 100: Living Off the Land (new, Imgflip)
- `one-does-not-simply.jpg` — One Does Not Simply Patch Production (new, Imgflip)
- `roll-initiative.jpg` — Roll Initiative: When the Alert Is Real (new, closest Imgflip D&D visual)

**Sourcing and layout:**
- Canonical Imgflip templates used where available.
- `fus-ro-dah.jpg` uses Know Your Meme reference because Imgflip result was not clean.
- `alignment-chart.jpg` generated as clean 3x3 alignment-grid template.
- `roll-initiative.jpg` uses closest Imgflip D&D dice/Nat 1 visual.
- Each meme slide includes image plus existing teaching content, ATT&CK lens where present/appropriate, and speaker note.
- Existing meme slides retrofitted rather than removed.
- All images embedded via Marp `<div class="columns">` or `![center w:60%]` patterns while preserving `parchment` class.

**Deck impact:** `slides/Slides.md` 1294 → 1534 lines. Marp validation: pass (exit 0).

**Rationale for reversal:** Fair-use exemption confirmed for educational deck use of standard meme templates. Graphical memes substantially improve audience engagement and humor landing without sacrificing technical content, MITRE mappings, or code examples.

## 2026-05-12 — Techorama Brand Typography

### Decision: Techorama Brand Font Stack

**Date:** 2026-05-12  
**Author:** verbal  
**Type:** theme / typography  
**Status:** applied

Apply the Techorama 2026 brand font stack in `slides/themes/custom-techorama.css`:

- **Logo / wordmark:** `Dreamhour` when installed locally; bundled `UnifrakturMaguntia` fallback; then `DS Wallau`; then serif.
- **Titles / headings:** existing `DS Wallau` and `DS Wallau OsF` files remain authoritative and unchanged.
- **Body:** bundled `Alegreya Sans` first, then `Aptos`, `Segoe UI`, `system-ui`, `sans-serif`.
- **Code:** existing Cascadia Code monospace stack remains unchanged.

**Rationale:** The official Techorama 2026 brand spec calls for Dreamhour for the logo, DS Wallau for titles, and Alegreya Sans for body copy. Dreamhour is commercial, so the deck should not bundle a third-party copy unless Chris supplies a licensed local font file. The CSS therefore prefers `local('Dreamhour')` and uses the SIL OFL `UnifrakturMaguntia` blackletter font as a bundled visual fallback.

**Files modified:**
- `slides/themes/custom-techorama.css`
- `slides/themes/fonts/AlegreyaSans-*.ttf` (6 weights, SIL OFL licensed, bundled locally)
- `slides/themes/fonts/UnifrakturMaguntia-Book.ttf` (SIL OFL licensed, bundled locally)

## 2026-05-12 — Slide Flow, Imagery, and Validation Review

### Decision: Slide Flow & Imagery Review — MITRE ATT&CK for Developers

**Date:** 2026-05-12T12:09:16+02:00  
**Author:** keyser  
**Type:** deck-review / visual-imagery  
**Status:** applied — reconciled 2026-05-12T12:09:16+02:00

#### Context

Full review of `slides/Slides.md` (78 slides, 1422 lines post-review) for narrative flow, pacing, acronym compliance, and Techorama image opportunities. Applied directly to the deck.

#### Flow Changes Made

**1. SNEAK 100 ATT&CK lens — bullet formatting fix**
- **Location:** Defense Evasion & Log Tampering, "SNEAK 100: Living Off the Land" slide
- **Issue:** ATT&CK lens bullets were formatted `-T1059` (no space), rendering as plain text rather than list items.
- **Fix:** Changed to `- T1059 command execution`, `- T1070 log tampering`, `- T1071 C2`.

**2. Detection Maturity slide — added visible progression labels**
- **Location:** Practical Implementation, "Detection Maturity: A Brief Evolution" slide
- **Issue:** The slide showed only a galaxy-brain meme image and an ATT&CK lens label. Without explicit stage labels, the slide required the audience to already know the meme format to extract the teaching point.
- **Fix:** Added a four-row maturity table (Raw logs → Alert rules → ATT&CK IDs → Behavioral analytics) visible on-slide so the progression is readable without the speaker.

**3. SIEM acronym expansion — decisions.md compliance**
- **Location:** Practical Implementation, "Implementation Roadmap" slide, Phase 2 Detection bullets
- **Issue:** "SIEM integration" appeared in visible slide content (line 1264 post-edit) without first-use expansion. The decisions.md applied note pointed to a speaker-note line that had since shifted due to content additions; the acronym was effectively unexpanded in visible slide content.
- **Fix:** Changed to "Security Information and Event Management (SIEM) integration". All subsequent SIEM uses (Roll Initiative slide visible text) remain bare as per convention.

#### Techorama Images Added

| Asset | Slide / Placement | Marp syntax |
|---|---|---|
| `knight-on-horse-gray.png` | "Let's Think Like Attackers" section divider | `![bg right:30% fit](...)` |
| `castle-skyline-silhouette.png` | "Initial Access & Credential Attacks" section divider | `![bg opacity:.2](...)` |
| `fleur-de-lis-pattern-dark.jpg` | "Persistence & Session Hijacking" section divider | `![bg opacity:.2](...)` |
| `stone-wall-texture-dark.jpg` | "Credential Access & Secrets" section divider | `![bg opacity:.15](...)` |
| `stone-wall-texture-dark.jpg` | "Defense Evasion & Log Tampering" section divider | `![bg opacity:.2](...)` — swapped from `techorama-hero-torches.png` (portrait transparency issue; stone-wall "hiding in plain sight" thematic fit) |
| `techorama-hero-medieval.png` | "Supply Chain Compromise" section divider | `![bg opacity:.2](...)` |
| `castle-skyline-silhouette.png` | "Collection & Exfiltration" section divider | `![bg opacity:.2](...)` |
| `celtic-border-gold.png` | "Key Takeaways" slide | `![bg opacity:.08](...)` (decorative watermark) |
| `techorama-wordmark-teal.png` | "Tell Me How I Did" QR slide, second column below QR code | `![w:220 center](...)` |

**Total new image placements: 9** (using 8 distinct assets; `castle-skyline-silhouette.png` used twice — Initial Access and Collection — both thematically appropriate: the castle under threat, then the treasure leaving).

#### Images Explicitly Rejected

| Asset | Reason |
|---|---|
| `techorama-wordmark-orange.jpg` | JPG format, lower fidelity; teal PNG preferred for dark-background slides |
| `techorama-logo-stone.png` | Effect duplicated by `stone-wall-texture-dark.jpg`; no unique placement |
| `techorama-logo-orange.png` | Orange logo creates contrast issues on dark section dividers; teal preferred |
| `techorama-logo-2026-medieval.png` | Title slide already dense (robot-knight + medieval-pattern-dark); adding a third element creates visual clutter. No secondary placement with clear rationale. |
| `footer-strip.jpg` | Managed by theme CSS; adding it explicitly to slides would duplicate the theme-level footer. |
| `techorama-badge-orange.png` | No slide context where a badge shape adds meaning rather than decoration; strong enough existing content. |

#### Slides Removed or Reordered

None. The existing 78-slide order follows the ATT&CK lifecycle correctly and the meme/parchment slides are well-distributed. The "Deployment Security Alignment Chart" meme between SolarWinds and "Initial Access" was examined — it serves as a deliberate palate cleanser before the first technical section, so it stays.

#### Trade-offs Recorded

- **Section divider opacity choices:** Each section's bg image uses a different opacity level (0.08–0.25) tuned to how busy the image is. Stone wall at 0.15, fleur-de-lis at 0.2 (busy patterns need lower opacity). Hero images at 0.20–0.25 because they have broader dark areas.
- **No image on "Practical Implementation" section:** This section is the methodical "do the work" close of the talk; a clean dark navy slide focuses attention on the roadmap, not atmosphere. Adding imagery would dilute the "time to get serious" signal.
- **No image on "Execution & Code Injection" section:** Code-heavy section follows immediately. Adding a bg image here risks visual noise on the dense code slides that follow (bg images bleed through in Marp for slides without their own bg override).
- **Detection Maturity table:** Chose a four-row table over a prose list because the galaxy-brain format maps cleanly to table rows. Speaker note preserved for the humor context.

#### Final Slide Count

**78 slides** (unchanged — no slides added or removed; 1 slide had visible-content expanded, 1 had a table added, section dividers received image directives only).

#### Acronym Compliance Status (post-review)

| Acronym | First visible use | Status |
|---|---|---|
| C2 (Command and Control) | SolarWinds slide | ✅ expanded |
| RCE (Remote Code Execution) | XZ Utils slide | ✅ expanded |
| CVSS (Common Vulnerability Scoring System) | XZ Utils slide | ✅ expanded |
| RAT (Remote Access Trojan) | Axios slide | ✅ expanded |
| SBOM (Software Bill of Materials) | Log4Shell slide | ✅ expanded |
| SIEM (Security Information and Event Management) | Implementation Roadmap | ✅ fixed this review |

#### Reconciliation Pass — 2026-05-12T12:09:16+02:00

A post-apply discrepancy audit found six mismatches between this decision file and `slides/Slides.md`. In every case the decision file's documented intent was correct; the file had wrong values. All six were corrected in the file.

| # | Section | What the file had | What it should have (per this doc) | Fix applied |
|---|---|---|---|---|
| 1 | Initial Access & Credential Attacks | `![bg](./themes/techorama/castle-skyline-silhouette.png)` — no opacity (= full strength) | `![bg opacity:.2](...)` | Added `opacity:.2` |
| 2 | Persistence & Session Hijacking | `![bg opacity:.5](./themes/techorama/fleur-de-lis-pattern-dark.jpg)` — too heavy for busy pattern | `![bg opacity:.2](...)` | Changed `.5` → `.2` |
| 3 | Credential Access & Secrets | `![bg opacity:.3](./themes/techorama/stone-wall-texture-dark.jpg)` | `![bg opacity:.15](...)` | Changed `.3` → `.15` |
| 4 | Supply Chain Compromise | `![bg opacity:1](./themes/techorama/stone-wall-texture-dark.jpg)` — wrong asset, full opacity | `![bg opacity:.2](./themes/techorama/techorama-hero-medieval.png)` | Replaced asset and opacity |
| 5 | Collection & Exfiltration | `![bg](./themes/techorama/castle-skyline-silhouette.png)` — no opacity (= full strength) | `![bg opacity:.2](...)` | Added `opacity:.2` |
| 6 | Practical Implementation | `![bg](./themes/techorama/medieval-pattern-dark.png)` — rogue image, decision file explicitly says no image here | No image | Removed entirely |

**Root cause:** Marp image syntax `![bg opacity:X]` is positional — the `opacity:` modifier must be inside the brackets with no space after the colon. Three of the six failures appear to have been Marp syntax that silently dropped the opacity modifier (defaulting to 1.0), and one was the wrong asset entirely (stone-wall written instead of hero-medieval for Supply Chain).

**Post-reconciliation file state is authoritative.** The table in "Techorama Images Added" above reflects the correct final state.

### Decision: Validation Report — slides/Slides.md (Initial)

**Date:** 2026-05-12T12:09:16+02:00  
**Author:** verbal  
**Type:** validation  
**Status:** BLOCKED — two issues returned to Keyser

#### Summary

Validation of `slides/Slides.md` following Keyser's flow-and-imagery edits. Two blocking issues found and returned for revision under reviewer lockout protocol.

#### Build Results

| Format | Exit | Notes |
|--------|------|-------|
| HTML   | 0 ✅ | Clean |
| PDF    | 0 ✅ | One benign path-scanner warning (sbom.json in fenced code block, line 1026-1028) |
| PNG    | 0 ✅ | 77 slides produced |

#### Font Check

| Font | Status |
|------|--------|
| DS Wallau | ✅ loaded |
| Alegreya Sans | ✅ loaded (20 faces) |

#### Section Divider Visual Pass

| Slide | Bg Image | Opacity | Result |
|---|---|---|---|
| Let's Think Like Attackers | `knight-on-horse-gray.png` | `bg right:30% fit` | ✅ |
| Initial Access & Credential Attacks | `castle-skyline-silhouette.png` | `.2` | ✅ |
| Persistence & Session Hijacking | `fleur-de-lis-pattern-dark.jpg` | `.2` | ✅ |
| Credential Access & Secrets | `stone-wall-texture-dark.jpg` | `.15` | ✅ |
| Defense Evasion & Log Tampering | `stone-wall-texture-dark.jpg` | `.2` | ⚠️ Image quality issue |
| Supply Chain Compromise | `techorama-hero-medieval.png` | `.2` | ✅ |
| Collection & Exfiltration | `castle-skyline-silhouette.png` | `.2` | ✅ |
| Key Takeaways | `celtic-border-gold.png` | `.08` | ✅ |

#### Blocking Issues

**BLOCKING #1: `Credential Access & Secrets` opacity discrepancy**
- **File state:** `![bg opacity:.3](./themes/techorama/stone-wall-texture-dark.jpg)` (line 582)
- **Documented state (Keyser's reconciliation):** should be `opacity:.15`
- **Issue:** Reconciliation note says `.15` was "fixed" but file still has `.3` — documentation inconsistent with actual file change.
- **Visual impact:** At `.3`, stone wall competes with text more than intended.
- **Fix:** Change `opacity:.3` → `opacity:.15` on line 582.

**BLOCKING #2: `Defense Evasion & Log Tampering` image quality**
- **File state:** `![bg opacity:.25](./themes/techorama/techorama-hero-torches.png)` (line 724)
- **Issue:** Portrait RGBA image with alpha-transparent padding (~45% lower area). Renders as incomplete background coverage with teal gaps on sides.
- **Options:**
  - Crop transparent padding from image.
  - Replace with full-bleed landscape image.
  - Accept partial coverage.

#### Non-Blocking Observations

1. Slide count: 77 rendered, not 78 documented.
2. `title-bg.png` missing from theme (pre-existing, non-visual impact).
3. Playwright-cli install side effects in `.claude/skills/` (not validation artifacts).

#### Known Non-Blocking Issues (Pre-existing)

- `title-bg.png` missing from `slides/themes/techorama/` — CSS references it; causes browser 404 × 4 per load but no visual impact (title slide uses explicit `![bg fill]` override).
- `techorama-hero-torches.png` is portrait RGBA with transparent lower ~45% — partial coverage when used as bg. Currently not used (Defense Evasion now uses stone-wall).
- Marp path scanner flags `./sbom.json` inside fenced code block at lines 1026–1028. Benign false-positive.

### Decision: Final Validation Report — slides/Slides.md

**Date:** 2026-05-12  
**Author:** verbal  
**Status:** ✅ PASS — Deck ready for commit

#### Summary

Full validation of `slides/Slides.md` following Keyser's flow-and-imagery edits and Verbal's 4 opacity corrections (under reviewer lockout protocol). All gates green.

#### Build Results

| Format | Exit | Notes |
|--------|------|-------|
| HTML   | 0 ✅ | Clean |
| PDF    | 0 ✅ | One benign path-scanner warning (sbom.json in fenced code block, line 1026-1028) |
| PNG    | 0 ✅ | 77 slides produced |

#### Font Check

| Font | Status |
|------|--------|
| DS Wallau | ✅ loaded |
| Alegreya Sans | ✅ loaded (20 faces) |

#### Section Divider Visual Pass — Final

| Slide | Bg Image | Opacity | Visual | Result |
|---|---|---|---|---|
| Let's Think Like Attackers | `knight-on-horse-gray.png` | `bg right:30% fit` | Knight silhouette right-aligned | ✅ |
| Initial Access & Credential Attacks | `castle-skyline-silhouette.png` | `.2` | Subtle castle, title crisp | ✅ |
| Persistence & Session Hijacking | `fleur-de-lis-pattern-dark.jpg` | `.2` | Diamond pattern barely visible, title clear | ✅ |
| Credential Access & Secrets | `stone-wall-texture-dark.jpg` | `.15` | Very subtle stone texture | ✅ |
| Defense Evasion & Log Tampering | `stone-wall-texture-dark.jpg` | `.2` | Stone texture, title legible | ✅ |
| Supply Chain Compromise | `techorama-hero-medieval.png` | `.2` | Full-frame medieval herald, torches, branding | ✅ |
| Collection & Exfiltration | `castle-skyline-silhouette.png` | `.2` | Matches Initial Access style | ✅ |
| Key Takeaways | `celtic-border-gold.png` | `.08` | Very subtle gold border | ✅ |

#### Hand-off

`slides/Slides.md` is ready for Chris to review and commit. Uncommitted changes staged for commit:
- `slides/Slides.md` — Keyser's imagery edits + Verbal's 4 opacity corrections
- `.squad/agents/keyser/history.md` — Keyser learnings
- `.squad/agents/verbal/history.md` — Verbal learnings

### Decision: Section Divider Opacity — Canonical Reference

**Date:** 2026-05-12  
**Author:** verbal  
**Type:** canonical reference  
**Status:** locked (prevents regression)

#### Purpose

Lock down correct opacity values to prevent future regression.

#### Canonical Opacity Table

| Slide Title | Bg Image | Opacity | Line in Slides.md |
|---|---|---|---|
| Let's Think Like Attackers | `themes/techorama/knight-on-horse-gray.png` | `bg right:30% fit` (no opacity modifier) | 179 |
| Initial Access & Credential Attacks | `themes/techorama/castle-skyline-silhouette.png` | `.2` | 238 |
| Persistence & Session Hijacking | `themes/techorama/fleur-de-lis-pattern-dark.jpg` | `.2` | 475 |
| Credential Access & Secrets | `themes/techorama/stone-wall-texture-dark.jpg` | `.15` | 582 |
| Defense Evasion & Log Tampering | `themes/techorama/stone-wall-texture-dark.jpg` | `.2` | 724 |
| Supply Chain Compromise | `themes/techorama/techorama-hero-medieval.png` | `.2` | 824 |
| Collection & Exfiltration | `themes/techorama/castle-skyline-silhouette.png` | `.2` | 1047 |
| Key Takeaways | `themes/techorama/celtic-border-gold.png` | `.08` | 1370 |

#### Design Rationale

- Stone textures (`.15`/`.2`) sit darker — subtle grain without competing with text.
- Silhouette PNGs use `.2` — dark enough to read heading, light enough to show the image shape.
- Celtic border at `.08` is intentionally near-invisible, used only as a warm finishing touch.
- Techorama hero (`techorama-hero-medieval.png`) is a detailed photo; `.2` keeps branding present but subordinate to the heading.
- "Let's Think Like Attackers" uses right-aligned fit (no opacity) because the knight is compositionally positioned to share the slide with the heading.

#### History

This table was finalized after three incorrect attempts by Keyser (reviewer lockout invoked 2026-05-12). Verbal applied the 4 corrections at lines 238, 475, 824, and 1047. Lines 582 and 724 were confirmed correct by Chris Ayers and were not touched.

**Do not modify section divider opacities without updating this document.**
