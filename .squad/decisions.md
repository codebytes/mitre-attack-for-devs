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
