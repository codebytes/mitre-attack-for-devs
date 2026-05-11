# Decision: Apply Techorama Theme to Live MITRE ATT&CK Deck

**Date:** 2026-05-11  
**Author:** verbal  
**Type:** theme-migration

## Summary

The live MITRE ATT&CK presentation at `slides/Slides.md` now uses `theme: custom-techorama` while preserving pagination and Chris Ayers' footer.

## Audit Findings

- Removed the old title-only `crooked-line-bg.svg` background and scoped white/green heading CSS because both were coupled to the previous MITRE visual system.
- Applied `title` to the opening slide and `section` to the major transition slides.
- No `_color` directives, inline styled color spans, Mermaid diagrams, or hardcoded table/background styles required migration.
- Existing scoped `pre` font-size adjustments on dense code slides remain valid with Techorama's dark code block styling.

## Validation

- HTML build passed.
- PDF build passed when rerun with `--browser-timeout 90` after the default 30s timeout.
- PNG build passed for all 68 slides.
- Playwright font validation passed for DS Wallau; console showed Font Awesome CDN font load errors and a benign favicon 404.
