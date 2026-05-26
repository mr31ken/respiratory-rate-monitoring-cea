#!/usr/bin/env python3
"""
build_supplementary_docx.py — Generate submission-ready Supplementary DOCX.
Uses python-docx. Times New Roman 11pt, 1.5 spacing.
Reads supplementary.md and converts to DOCX programmatically.
"""

import os, re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

ROOT = Path(__file__).resolve().parent.parent
SUPP = ROOT / "supplementary"
OUTPUT = SUPP / "supplementary_20260526.docx"

FONT_NAME = "Times New Roman"
FONT_SIZE = 10
LINE_SPACING = WD_LINE_SPACING.ONE_POINT_FIVE


def set_run_font(run, name=FONT_NAME, size=FONT_SIZE, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def add_para(doc, text="", bold=False, italic=False, alignment=None,
             space_after=None, space_before=None, first_line_indent=None,
             left_indent=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, bold=bold, italic=italic)
    fmt = p.paragraph_format
    fmt.line_spacing_rule = LINE_SPACING
    if alignment:
        fmt.alignment = alignment
    if space_after is not None:
        fmt.space_after = Pt(space_after)
    if space_before is not None:
        fmt.space_before = Pt(space_before)
    if first_line_indent is not None:
        fmt.first_line_indent = Inches(first_line_indent)
    if left_indent is not None:
        fmt.left_indent = Inches(left_indent)
    return p


def add_mixed(doc, parts, alignment=None, first_line_indent=None,
              left_indent=None, space_before=None, space_after=None,
              hanging_indent=None):
    """parts: list of (text, bold, italic) OR (text, bold, italic, code)."""
    p = doc.add_paragraph()
    for part in parts:
        if len(part) == 4:
            text, bold, italic, code = part
        else:
            text, bold, italic = part
            code = False
        run = p.add_run(text)
        if code:
            set_run_font(run, name="Consolas", size=10, bold=bold, italic=italic)
        else:
            set_run_font(run, bold=bold, italic=italic)
    fmt = p.paragraph_format
    fmt.line_spacing_rule = LINE_SPACING
    if alignment:
        fmt.alignment = alignment
    if first_line_indent is not None:
        fmt.first_line_indent = Inches(first_line_indent)
    if left_indent is not None:
        fmt.left_indent = Inches(left_indent)
    if hanging_indent is not None:
        fmt.first_line_indent = Inches(-hanging_indent)
    if space_before is not None:
        fmt.space_before = Pt(space_before)
    if space_after is not None:
        fmt.space_after = Pt(space_after)
    return p


# ── Inline markdown parser ───────────────────────────────────────────
_INLINE_RE = re.compile(
    r"(`[^`\n]+`)"
    r"|(\*\*[^*\n]+?\*\*)"
    r"|(\*(?=\S)[^*\n]+?(?<=\S)\*)"
)


def _split_inline_md(text):
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
    for seg in segments:
        if len(seg) == 4:
            text, bold, italic, code = seg
        else:
            text, bold, italic = seg
            code = False
        if not text:
            continue
        run = paragraph.add_run(text)
        if code:
            set_run_font(run, name="Consolas", size=10,
                         bold=bold or base_bold, italic=italic or base_italic)
        else:
            set_run_font(run, bold=bold or base_bold,
                         italic=italic or base_italic)
    return paragraph


def add_inline(doc, text, alignment=None, first_line_indent=None,
               left_indent=None, hanging_indent=None,
               space_before=None, space_after=None,
               base_bold=False, base_italic=False):
    p = doc.add_paragraph()
    segments = _split_inline_md(text)
    if not segments:
        run = p.add_run("")
        set_run_font(run, bold=base_bold, italic=base_italic)
    else:
        _add_styled_runs(p, segments, base_bold=base_bold, base_italic=base_italic)
    fmt = p.paragraph_format
    fmt.line_spacing_rule = LINE_SPACING
    if alignment:
        fmt.alignment = alignment
    if first_line_indent is not None:
        fmt.first_line_indent = Inches(first_line_indent)
    if left_indent is not None:
        fmt.left_indent = Inches(left_indent)
    if hanging_indent is not None:
        fmt.first_line_indent = Inches(-hanging_indent)
    if space_before is not None:
        fmt.space_before = Pt(space_before)
    if space_after is not None:
        fmt.space_after = Pt(space_after)
    return p


def add_bullet(doc, text, level_indent=0.4):
    segments = _split_inline_md(text)
    p = doc.add_paragraph()
    bullet_run = p.add_run("• ")
    set_run_font(bullet_run)
    _add_styled_runs(p, segments)
    fmt = p.paragraph_format
    fmt.line_spacing_rule = LINE_SPACING
    fmt.left_indent = Inches(level_indent)
    fmt.first_line_indent = Inches(-0.25)
    return p


def add_heading_centered(doc, text):
    return add_para(doc, text, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                    space_before=12, space_after=6)


def add_subheading(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, bold=True, italic=True)
    fmt = p.paragraph_format
    fmt.line_spacing_rule = LINE_SPACING
    fmt.space_before = Pt(6)
    fmt.space_after = Pt(3)
    return p


def add_body(doc, text, indent=True):
    return add_para(doc, text, first_line_indent=0.4 if indent else None)


def _add_cell_styled(cell, text, base_bold=False, size=9):
    """Render markdown-inline text into a table cell as styled runs."""
    cell.text = ""
    para = cell.paragraphs[0]
    segments = _split_inline_md(text)
    if not segments:
        run = para.add_run("")
        set_run_font(run, bold=base_bold, size=size)
        return
    for seg in segments:
        if len(seg) == 4:
            t, b, i, code = seg
        else:
            t, b, i = seg
            code = False
        if not t:
            continue
        run = para.add_run(t)
        if code:
            set_run_font(run, name="Consolas", size=size,
                         bold=b or base_bold, italic=i)
        else:
            set_run_font(run, bold=b or base_bold, italic=i, size=size)


def flush_table(doc, rows):
    if not rows:
        return
    headers = [c.strip() for c in rows[0].split("|") if c.strip()]
    data = []
    for row in rows[2:]:  # skip separator
        cells = [c.strip() for c in row.split("|") if c.strip()]
        if cells:
            data.append(cells)
    if not headers or not data:
        return
    ncols = len(headers)
    table = doc.add_table(rows=1 + len(data), cols=ncols)
    table.style = "Table Grid"
    # Header row
    for j, h in enumerate(headers):
        _add_cell_styled(table.rows[0].cells[j], h, base_bold=True, size=9)
    # Data rows
    for i, row_data in enumerate(data):
        for j in range(min(len(row_data), ncols)):
            _add_cell_styled(table.rows[i + 1].cells[j], row_data[j], size=9)


# ── Read markdown ────────────────────────────────────────────────────
md_text = (SUPP / "supplementary_20260526.md").read_text(encoding="utf-8")

doc = Document()

# Page setup
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11)
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

# Page numbers (footer)
footer = section.footer
footer.is_linked_to_previous = False
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run()
run.font.name = FONT_NAME
run.font.size = Pt(10)
fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
run._r.append(fldChar1)
run2 = fp.add_run()
instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
run2._r.append(instrText)
run3 = fp.add_run()
fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
run3._r.append(fldChar2)

# Running header
header = section.header
header.is_linked_to_previous = False
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run_h = hp.add_run("Supplementary Materials — Economic Evaluation of Automated RR Monitoring")
run_h.font.name = FONT_NAME
run_h.font.size = Pt(8)
run_h.italic = True

# Default style
style = doc.styles['Normal']
style.font.name = FONT_NAME
style.font.size = Pt(FONT_SIZE)
style.paragraph_format.line_spacing_rule = LINE_SPACING

# ══════════════════════════════════════════════════════════════════════
# Parse markdown into sections
# ══════════════════════════════════════════════════════════════════════
lines = md_text.split("\n")
sections_list = []
current_heading = ""
current_lines = []

for line in lines:
    if line.startswith("# ") and not line.startswith("## "):
        if current_heading or current_lines:
            sections_list.append((current_heading, current_lines))
        current_heading = line[2:].strip()
        current_lines = []
    elif line.startswith("## "):
        if current_heading or current_lines:
            sections_list.append((current_heading, current_lines))
        current_heading = line[3:].strip()
        current_lines = []
    else:
        current_lines.append(line)

if current_heading or current_lines:
    sections_list.append((current_heading, current_lines))

# ══════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════

add_para(doc, "SUPPLEMENTARY MATERIALS", bold=True,
         alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
add_para(doc, "", space_after=6)
add_para(doc, "Economic Evaluation of Automated Respiratory Rate Monitoring",
         bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
add_para(doc, "in General Hospital Wards:",
         bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
add_para(doc, "A Deterministic Cost-Minimization and Break-Even Modeling Study",
         bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

# JCMC requires each SI file to include article title, journal, authors,
# affiliations, and corresponding author contact. Extract this block from the
# markdown (it sits as the body of the long-title heading section).
title_heading = ("Economic Evaluation of Automated Respiratory Rate Monitoring "
                 "in General Hospital Wards: A Deterministic Cost-Minimization "
                 "and Break-Even Modeling Study")
header_block = next((c for h, c in sections_list if h == title_heading), None)
if header_block:
    for line in header_block:
        s = line.strip()
        if not s or s == "---":
            continue
        # Strip markdown link syntax [text](url) -> text
        s_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        # Bold label "**Label:** value" pattern (Target Journal / Authors /
        # Corresponding author)
        m = re.match(r'^\*\*(.+?):\*\*\s*(.*)', s_clean)
        if m:
            add_mixed(doc,
                      [(m.group(1) + ": ", True, False),
                       (m.group(2), False, False)],
                      alignment=WD_ALIGN_PARAGRAPH.CENTER,
                      space_before=4, space_after=4)
        elif s_clean[0] in "¹²³⁴⁵⁶⁷⁸⁹":
            # Affiliation lines
            add_para(doc, s_clean,
                     alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
        else:
            add_para(doc, s_clean,
                     alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════
# Process each section
# ══════════════════════════════════════════════════════════════════════

skip_sections = {
    "Supplementary Materials",
    "Economic Evaluation of Automated Respiratory Rate Monitoring in General Hospital Wards: A Deterministic Cost-Minimization and Break-Even Modeling Study",
}

for heading, content_lines in sections_list:
    if heading in skip_sections:
        continue
    if not heading and all(l.strip() in ("", "---") for l in content_lines):
        continue

    # Section heading
    if heading:
        add_heading_centered(doc, heading)

    # Process content
    in_table = False
    table_rows = []
    paragraph_buffer = ""

    def flush_paragraph(doc, text):
        if not text.strip():
            return
        text = text.strip()

        # Italic-only standalone line: render fully italic
        if (text.startswith("*") and text.endswith("*")
                and not text.startswith("**") and not text.endswith("**")
                and text.count("*") == 2):
            inner = text[1:-1]
            add_inline(doc, inner, base_italic=True)
            return

        # Bullet line — render with inline md parsing
        if text.startswith("- "):
            add_bullet(doc, text[2:], level_indent=0.4)
            return

        # Reference line "[1] Author. Title..." — hanging indent
        ref_match = re.match(r'^\[(\d+)\]\s+(.*)', text)
        if ref_match:
            p = doc.add_paragraph()
            label_run = p.add_run(f"[{ref_match.group(1)}] ")
            set_run_font(label_run)
            _add_styled_runs(p, _split_inline_md(ref_match.group(2)))
            fmt = p.paragraph_format
            fmt.line_spacing_rule = LINE_SPACING
            fmt.left_indent = Inches(0.4)
            fmt.first_line_indent = Inches(-0.4)
            return

        # Numbered list with bold label
        m_numbold = re.match(r'^(\d+\.\s+)\*\*(.+?)\*\*\s*(.*)', text)
        if m_numbold:
            num = m_numbold.group(1)
            label = m_numbold.group(2)
            rest = m_numbold.group(3)
            p = doc.add_paragraph()
            run = p.add_run(num + label)
            set_run_font(run, bold=True)
            if rest:
                rest_prefix = p.add_run(" ")
                set_run_font(rest_prefix)
                _add_styled_runs(p, _split_inline_md(rest))
            fmt = p.paragraph_format
            fmt.line_spacing_rule = LINE_SPACING
            fmt.left_indent = Inches(0.4)
            return

        first_indent = 0.4
        if text.startswith("**"):
            first_indent = None
        add_inline(doc, text, first_line_indent=first_indent)

    for line in content_lines:
        stripped = line.strip()

        if stripped == "---":
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            continue

        if stripped.startswith("```"):
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            continue

        # Table detection
        if "|" in stripped and stripped.startswith("|"):
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table(doc, table_rows)
            in_table = False
            table_rows = []

        # Subheading
        if stripped.startswith("### "):
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            add_subheading(doc, stripped[4:])
            continue

        if stripped.startswith("#### "):
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            add_subheading(doc, stripped[5:])
            continue

        # Empty line = paragraph break
        if not stripped:
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            continue

        # Bullet line: flush buffer first so bullets are their own paragraphs
        if stripped.startswith("- "):
            if paragraph_buffer:
                flush_paragraph(doc, paragraph_buffer)
                paragraph_buffer = ""
            flush_paragraph(doc, stripped)
            continue

        # Accumulate
        if paragraph_buffer:
            paragraph_buffer += " " + stripped
        else:
            paragraph_buffer = stripped

    # Flush remaining
    if paragraph_buffer:
        flush_paragraph(doc, paragraph_buffer)
    if in_table and table_rows:
        flush_table(doc, table_rows)

    # Page break after each S-section
    if heading and heading.startswith("S"):
        doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════

doc.save(str(OUTPUT))
print(f"Saved: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size / 1024:.0f} KB")
