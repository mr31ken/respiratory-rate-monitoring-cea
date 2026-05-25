#!/usr/bin/env python3
"""Build cover letter DOCX from markdown source."""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "cover_letter_20260516.md"
OUT = ROOT / "cover_letter_20260516.docx"

text = SRC.read_text(encoding="utf-8")

doc = Document()

# Page margins
section = doc.sections[0]
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)

# Default style
style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(11)

# ── Inline markdown parser (shared logic with build_docx/supplementary) ──
_INLINE_RE = re.compile(
    r"(`[^`\n]+`)"                  # 1) `code`
    r"|(\*\*[^*\n]+?\*\*)"          # 2) **bold**
    r"|(\*(?=\S)[^*\n]+?(?<=\S)\*)" # 3) *italic*
)


def _split_inline_md(text):
    """Return a list of (text, bold, italic, code) tuples."""
    if not text:
        return []
    out = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False, False, False))
        token = m.group(0)
        if token.startswith("`"):
            out.append((token[1:-1], False, False, True))
        elif token.startswith("**"):
            out.append((token[2:-2], True, False, False))
        else:
            out.append((token[1:-1], False, True, False))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, False, False))
    merged = []
    for seg in out:
        if merged and not (seg[1] or seg[2] or seg[3]) and not (merged[-1][1] or merged[-1][2] or merged[-1][3]):
            merged[-1] = (merged[-1][0] + seg[0], False, False, False)
        else:
            merged.append(seg)
    return merged


def _add_styled_runs(paragraph, segments, base_bold=False, base_italic=False):
    """Append styled runs to a python-docx paragraph."""
    for seg in segments:
        if len(seg) == 4:
            text, bold, italic, code = seg
        else:
            text, bold, italic = seg
            code = False
        if not text:
            continue
        run = paragraph.add_run(text)
        run.bold = bold or base_bold
        run.italic = italic or base_italic
        if code:
            run.font.name = "Consolas"
            run.font.size = Pt(10)
    return paragraph


def add_runs(paragraph, line):
    """Process inline backticks, bold (**...**), and italic (*...*) markers."""
    _add_styled_runs(paragraph, _split_inline_md(line))

lines = text.splitlines()
i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if not line:
        # Add empty paragraph for spacing
        doc.add_paragraph()
    elif line.startswith("- "):
        # Bullet item
        para = doc.add_paragraph(style="List Bullet")
        add_runs(para, line[2:])
    elif line.startswith(("1. ", "2. ", "3. ")):
        # Numbered item
        para = doc.add_paragraph(style="List Number")
        add_runs(para, line[3:])
    elif re.match(r"^\s+\*Justification:\*", line):
        # Indented italic justification
        para = doc.add_paragraph()
        para.paragraph_format.left_indent = Inches(0.5)
        add_runs(para, line.strip())
    else:
        para = doc.add_paragraph()
        add_runs(para, line)
    i += 1

doc.save(OUT)
print(f"Saved: {OUT}")
print(f"Size: {OUT.stat().st_size / 1024:.1f} KB")
