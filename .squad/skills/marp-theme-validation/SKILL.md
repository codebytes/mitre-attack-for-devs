---
name: marp-theme-validation
description: Validate Marp themes with Marp CLI builds plus Playwright browser checks
domain: marp-theming
confidence: high
source: verbal (2026-05-11)
---

# Skill: Marp Theme Validation

Use this after creating or changing a Marp CSS theme. It catches syntax errors, missing local assets, PDF/rasterization issues, and browser-only font/path problems.

## 1. Audit Before Running Tools

- Confirm `/* @theme theme-name */` matches the deck frontmatter.
- Confirm braces/selectors are balanced.
- Confirm every local `url(...)` target exists from the deck/output path Marp will serve. For decks in `slides/`, local theme assets usually need `themes/...` URLs once CSS is embedded into HTML.
- Confirm every sample deck `_class` has a matching `section.<class>` rule.

## 2. Marp CLI Builds

Put the markdown input before `--theme-set`; `--theme-set` is an array option and can swallow following positional arguments if placed first.

```bash
mkdir -p validation-artifacts
npx --package @marp-team/marp-cli marp slides/sample.md \
  --theme-set slides/themes/custom-theme.css \
  -o validation-artifacts/preview.html --html

npx --package @marp-team/marp-cli marp slides/sample.md \
  --theme-set slides/themes/custom-theme.css \
  --pdf -o validation-artifacts/preview.pdf --allow-local-files

npx --package @marp-team/marp-cli marp slides/sample.md \
  --theme-set slides/themes/custom-theme.css \
  --images png --image-scale 1 --browser-timeout 90 \
  -o validation-artifacts/slide --allow-local-files
```

Treat `Some of the local files are missing` as a defect unless it is proven unrelated.

## 3. Browser Validation with Playwright

Serve the repo root, load the generated preview, wait for fonts, and check computed styles.

```bash
npx http-server -p 8765 -c-1 --cors -s
```

Playwright checks to run:

- `await page.evaluate(() => document.fonts.ready)`
- `document.fonts.check('16px "Font Name"')`
- `Array.from(document.fonts)` shows the expected custom `FontFace` entry with `status: 'loaded'`
- computed `font-family` for title `h1`
- computed background color for the first themed slide
- console errors after reload
- full-page and per-slide screenshots

## Gotchas

- Marp embeds CSS into the generated HTML. Local CSS `url(...)` paths resolve from the HTML/deck location during browser/PDF/image conversion, not necessarily from the CSS file location.
- Marp PNG export can time out at the default 30 seconds when fonts/images are involved; retry with `--browser-timeout 90`.
- Browser favicon 404s are not theme defects unless a favicon is part of the theme requirements.
