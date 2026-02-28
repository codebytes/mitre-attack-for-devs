"""Extract code blocks from Slides.md and render them as syntax-highlighted PNG images."""
import re
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter


SLIDES_PATH = "slides/Slides.md"
IMG_DIR = "slides/img/code"
# Dark theme matching slides
STYLE = "monokai"
FONT_SIZE = 14
LINE_PAD = 4
LINE_NUMBERS = False


def extract_code_blocks(md_path):
    """Extract all fenced code blocks with their language and line numbers."""
    content = open(md_path, "r", encoding="utf-8").read()
    blocks = []
    pattern = re.compile(r'^```(\w+)\n(.*?)^```', re.MULTILINE | re.DOTALL)
    for i, m in enumerate(pattern.finditer(content)):
        lang = m.group(1)
        code = m.group(2).rstrip('\n')
        start = content[:m.start()].count('\n') + 1
        blocks.append({
            'id': f'code-{i+1:02d}',
            'lang': lang,
            'code': code,
            'start_line': start,
            'match_start': m.start(),
            'match_end': m.end(),
            'original': m.group(0),
        })
    return blocks, content


def render_code_image(block, outdir):
    """Render a code block to a PNG image using Pygments."""
    lang_map = {'csharp': 'c#', 'javascript': 'js'}
    lang = lang_map.get(block['lang'], block['lang'])
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = get_lexer_by_name('text')

    formatter = ImageFormatter(
        style=STYLE,
        font_size=FONT_SIZE,
        line_pad=LINE_PAD,
        line_numbers=LINE_NUMBERS,
        image_pad=16,
        font_name="Consolas",
    )
    img_data = highlight(block['code'], lexer, formatter)
    img_path = os.path.join(outdir, f"{block['id']}.png")
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def replace_code_blocks(content, blocks, img_dir_rel="img/code"):
    """Replace code blocks in markdown with image references."""
    # Process in reverse order to preserve positions
    for block in reversed(blocks):
        img_tag = f'<img src="{img_dir_rel}/{block["id"]}.png" alt="{block["lang"]} code" style="width: 900px; max-height: 75%; margin: 0 auto; display: block;" />'
        content = content[:block['match_start']] + img_tag + content[block['match_end']:]
    return content


if __name__ == "__main__":
    os.makedirs(IMG_DIR, exist_ok=True)

    blocks, content = extract_code_blocks(SLIDES_PATH)
    print(f"Found {len(blocks)} code blocks")

    for b in blocks:
        path = render_code_image(b, IMG_DIR)
        lines = b['code'].count('\n') + 1
        print(f"  {b['id']}: {b['lang']:12s} {lines:3d} lines -> {path}")

    new_content = replace_code_blocks(content, blocks)
    with open(SLIDES_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"\nUpdated {SLIDES_PATH} with {len(blocks)} image references")
