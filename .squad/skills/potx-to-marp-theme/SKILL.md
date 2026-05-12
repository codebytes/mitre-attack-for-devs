---
name: potx-to-marp-theme
description: Extract design tokens from .potx/.pptx PowerPoint templates into Marp CSS themes
domain: marp-theming
confidence: high
source: verbal (2026-05-11)
---

# Skill: Converting .potx Templates to Marp Themes

## Context

Speaker-conference templates come as `.potx` (PowerPoint template) files. This skill captures the repeatable process for turning one into a working Marp CSS theme.

## Key Insight

A `.potx` file is a ZIP archive. Unzip it to inspect design XML, extract color tokens, identify structural images, and map them to CSS variables.

---

## Step-by-Step Process

### 1. Extract the Archive

```bash
# NOTE: /tmp is forbidden in this project. Use a path inside the repo.
mkdir -p slides/themes/.potx-extract
unzip -q "path/to/Template.potx" -d slides/themes/.potx-extract
```

Clean up after you're done:
```bash
rm -rf slides/themes/.potx-extract
```

---

### 2. Parse Design Tokens from `ppt/theme/theme1.xml`

The key color nodes inside `<a:clrScheme>`:

```
dk1  → darkest text (usually windowText / #000000)
lt1  → lightest bg  (usually window    / #FFFFFF)
dk2  → primary dark background accent (a:srgbClr val="XXXXXX")
lt2  → secondary light background
accent1-6 → brand palette colors
hlink → hyperlink color
```

Use Python to extract quickly:

```python
import re

with open('slides/themes/.potx-extract/ppt/theme/theme1.xml') as f:
    data = f.read()

colors = re.findall(r'<a:srgbClr val="([A-Fa-f0-9]{6})"', data)
print(sorted(set(colors)))
```

---

### 3. Identify Font Families

In `<a:fontScheme>`:
- `<a:majorFont>` → heading/display font (e.g., "Aptos Display")
- `<a:minorFont>` → body font (e.g., "Aptos")

Map `majorFont` to the custom display font you're bringing in (e.g., DS Wallau).
Map `minorFont` → safe system font stack fallback.

---

### 4. Map Slide Layouts to Structural Images

```python
import xml.etree.ElementTree as ET

# Resolve which images each layout uses via its _rels file
tree = ET.parse('slides/themes/.potx-extract/ppt/slideLayouts/_rels/slideLayout1.xml.rels')
root = tree.getroot()
for rel in root:
    print(rel.attrib.get('Id'), rel.attrib.get('Target'))
```

Common pattern:
- `slideLayout1` = Title slide → typically uses 2 images (full-bg + decorative graphic)
- `slideLayout2-3` = Section/content backgrounds → 1-2 images
- `slideLayout4+` = Standard content → shared footer/accent strip

---

### 5. Sample Image Colors (for non-schemed backgrounds)

When images carry brand color (not just stock photos), sample them:

```python
import zlib, struct

def find_nonblack_colors(path, max_check=5000):
    with open(path, 'rb') as f:
        data = f.read()
    w = struct.unpack('>I', data[16:20])[0]
    h = struct.unpack('>I', data[20:24])[0]
    color_type = data[25]
    idat = b''
    pos = 8
    while pos < len(data) - 12:
        length = struct.unpack('>I', data[pos:pos+4])[0]
        chunk_type = data[pos+4:pos+8]
        if chunk_type == b'IDAT':
            idat += data[pos+8:pos+8+length]
        pos += 12 + length
    raw = zlib.decompress(idat)
    bpp = 4 if color_type == 6 else 3
    row_size = 1 + w * bpp
    colors = {}
    checked = 0
    for i in range(h):
        for x in range(0, w, max(1, w//50)):
            px = i * row_size + 1 + x * bpp
            r, g, b = raw[px], raw[px+1], raw[px+2]
            a = raw[px+3] if bpp == 4 else 255
            if a > 10 and (r > 5 or g > 5 or b > 5):
                hex_c = f'#{r:02X}{g:02X}{b:02X}'
                colors[hex_c] = colors.get(hex_c, 0) + 1
            checked += 1
            if checked > max_check:
                break
        if checked > max_check:
            break
    return sorted(colors.items(), key=lambda x: -x[1])[:10]
```

Large files (>1MB) are almost always stock photos — skip them.

---

### 6. Select Assets to Copy

Copy to `slides/themes/<conference-name>/`:
- ✅ Full-slide backgrounds (1280x720 or 1600x900 in px)
- ✅ Logo-sized images (portrait aspect, < 100KB usually)
- ✅ Footer/accent strips (wide + short, e.g., 1600x288)
- ❌ Stock photos (>1MB, people or nature imagery)
- ❌ `.emf` vector files (not supported in CSS/HTML)

---

### 7. Create the CSS Theme

Follow the `custom-mitre-attack.css` structure:
1. Comment block: `/* @theme custom-XXXX */`
2. `@import 'default';` as base
3. `@font-face` blocks for custom fonts (relative paths)
4. `:root {}` CSS variables for all design tokens
5. `section` base styles (font, size, padding, border-top accent)
6. Headings, links, lists, blockquotes, code blocks, tables
7. Slide variants: `section.title`, `section.section`, `section.lead`, `section.invert`

---

### 8. Smoke Test

```bash
npx --yes @marp-team/marp-cli \
  --theme-set slides/themes/custom-XXXX.css \
  --output slides/preview.html \
  slides/sample.md
```

A clean exit (no errors in stderr) confirms the CSS is valid and the theme registers correctly.

---

## Anti-Patterns

- **Don't copy `.emf` files** — not renderable in browser/CSS
- **Don't reference absolute paths** in the CSS — always relative to the theme file
- **Don't import stock photos** — they bloat the repo and aren't used by CSS
- **Don't forget to clean up the extraction directory** — it's temporary

## Files Produced

```
slides/themes/
├── custom-XXXX.css          ← theme CSS (registered via --theme-set)
├── fonts/
│   └── CustomFont.ttf       ← display font
└── XXXX/
    ├── title-bg.png         ← title slide background
    ├── content-bg.png       ← content slide background
    ├── footer-strip.jpg     ← accent strip
    └── logo.png             ← conference logo
slides/
└── XXXX-sample.md           ← sample deck for preview
```
