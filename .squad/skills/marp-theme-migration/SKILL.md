---
name: marp-theme-migration
description: Apply an existing Marp theme to an existing deck without breaking theme-coupled slide content
confidence: high
source: verbal (2026-05-11)
---

# Skill: Marp Theme Migration

Use this when moving an existing Marp deck from one theme to another.

## Process

1. **Read the target theme first**
   - Confirm `/* @theme ... */`, available slide classes, font assets, color tokens, and code/table/image defaults.
   - Identify whether the default slide is light or dark; do not assume every branded theme uses one background everywhere.

2. **Audit the deck for theme coupling**
   - Frontmatter `theme:` value.
   - Background directives: `![bg]`, `![bg left]`, `![bg right]`.
   - Marp directives: `_class`, `_color`, `_backgroundColor`, `_footer`, `_header`.
   - Scoped CSS blocks and inline HTML styles, especially `color`, `background`, text shadows, and code sizing.
   - Mermaid diagrams, tables, blockquotes, custom columns, and full-slide images.

3. **Map slide intent to target classes**
   - Opening/title slide → target theme's title class.
   - Major transition slides → section divider class.
   - Quote/callout slides → lead/invert class only when contrast and layout improve.
   - Keep normal content slides on default layout unless the theme explicitly expects all-dark content.

4. **Migrate surgically**
   - Remove old theme-specific backgrounds or scoped colors when the new class provides the visual treatment.
   - Preserve content, speaker notes, pagination, and author footer unless explicitly requested.
   - Keep scoped sizing CSS only when it solves dense content overflow and remains legible in the new theme.

5. **Validate with builds and visual checks**
   - Build HTML, PDF, and PNG with the new `--theme-set`.
   - If PDF/image conversion times out at the default 30s, retry with `--browser-timeout 90` before treating it as a theme defect.
   - Spot-check title, section divider, dense code, table, image, and final slides.
   - Use Playwright to verify custom fonts and console errors.

## Red Flags

- White text or bright accent colors left from the old deck on a new light default layout.
- Old background images fighting the new theme's title or section backgrounds.
- SVG/diagram text hardcoded for the opposite background color.
- Remote icon-font dependencies that do not load in offline validation.
