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
