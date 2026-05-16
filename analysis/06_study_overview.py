#!/usr/bin/env python3
"""
06_study_overview.py
--------------------
Generate Figure 1: Study Overview — a flow-diagram summarising the
study methodology (literature search, model construction, analysis).

Outputs:
  ../figures/fig1_study_overview.pdf
  ../figures/fig1_study_overview.png
"""

import pathlib
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["pdf.fonttype"] = 42

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

# ── Colour palette (muted, journal-friendly) ───────────────────────
COL_LIT   = "#4878A8"   # steel blue  — literature search
COL_MODEL = "#D4763A"   # burnt orange — model construction
COL_ANAL  = "#5A9E6F"   # sage green  — analysis
COL_BG    = "#F7F7F7"   # light grey background for sections
COL_TEXT  = "#2C2C2C"   # near-black text
COL_ARROW = "#555555"   # arrow colour
WHITE     = "#FFFFFF"

# ── Helper: draw a rounded box with centred text ───────────────────
def draw_box(ax, x, y, w, h, text, facecolor=WHITE, edgecolor=COL_TEXT,
             fontsize=7.5, fontweight="normal", text_color=COL_TEXT,
             linewidth=1.0, zorder=3):
    """Draw a rounded rectangle and place centred text inside."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02",
        facecolor=facecolor, edgecolor=edgecolor,
        linewidth=linewidth, zorder=zorder,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fontsize,
        fontweight=fontweight, color=text_color,
        zorder=zorder + 1, linespacing=1.35,
        wrap=False,
    )
    return box


def draw_arrow(ax, x0, y0, x1, y1, color=COL_ARROW):
    """Draw a simple arrow between two points."""
    ax.annotate(
        "", xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            linewidth=1.3,
            shrinkA=2, shrinkB=2,
        ),
        zorder=2,
    )


def draw_section_bg(ax, x, y, w, h, label, color):
    """Draw a labelled background rectangle for a section."""
    bg = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015",
        facecolor=color, edgecolor="none",
        alpha=0.12, zorder=0,
    )
    ax.add_patch(bg)
    # Section header
    ax.text(
        x + w / 2, y + h + 0.015, label,
        ha="center", va="bottom", fontsize=9, fontweight="bold",
        color=color, zorder=1,
    )


# ══════════════════════════════════════════════════════════════════════
# Build figure
# ══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ── Layout constants ────────────────────────────────────────────────
# Three columns: literature (left), model (centre), analysis (right)
SEC_PAD = 0.02
BOX_H   = 0.10   # standard box height
GAP_Y   = 0.04   # vertical gap between stacked boxes

# Section backgrounds
draw_section_bg(ax, 0.02, 0.08, 0.27, 0.80, "Literature Search", COL_LIT)
draw_section_bg(ax, 0.345, 0.08, 0.29, 0.80, "Model Construction", COL_MODEL)
draw_section_bg(ax, 0.695, 0.08, 0.28, 0.80, "Analysis", COL_ANAL)

# ====================================================================
# SECTION 1 — Literature Search
# ====================================================================
bx, bw = 0.04, 0.23

# Databases searched
db_y = 0.68
draw_box(ax, bx, db_y, bw, 0.16,
         "Database Search\n\nPubMed\nNICE  |  FDA 510(k)\nPMDA  |  Gov Statistics",
         edgecolor=COL_LIT, fontsize=7)

# Arrow down
draw_arrow(ax, bx + bw/2, db_y, bx + bw/2, db_y - GAP_Y + 0.005)

# Screening
scr_y = db_y - BOX_H - GAP_Y
draw_box(ax, bx, scr_y, bw, BOX_H,
         "Device Identification\n& Screening",
         edgecolor=COL_LIT, fontsize=7.5)

# Arrow down
draw_arrow(ax, bx + bw/2, scr_y, bx + bw/2, scr_y - GAP_Y + 0.005)

# Result
res_y = scr_y - BOX_H - GAP_Y
draw_box(ax, bx, res_y, bw, BOX_H,
         "9 Devices\n5 Technology Categories",
         facecolor=COL_LIT, edgecolor=COL_LIT,
         fontsize=8, fontweight="bold", text_color=WHITE)

# Technology categories annotation
cat_y = res_y - 0.13
draw_box(ax, bx, cat_y, bw, 0.12,
         "Pulse-oximetry | Impedance\nCapnography | Non-contact\n(radar / under-mattress) | Wearable",
         edgecolor=COL_LIT, fontsize=6.5)
draw_arrow(ax, bx + bw/2, res_y, bx + bw/2, cat_y + 0.12 + 0.005)

# ====================================================================
# SECTION 2 — Model Construction
# ====================================================================
mx, mw = 0.37, 0.245

# Comparator
comp_y = 0.72
draw_box(ax, mx, comp_y, mw, 0.12,
         "Comparator\n\nManual RR Counting\nvs 5 Automated Scenarios",
         edgecolor=COL_MODEL, fontsize=7)

# Arrow down
draw_arrow(ax, mx + mw/2, comp_y, mx + mw/2, comp_y - GAP_Y + 0.005)

# Perspective
persp_y = comp_y - BOX_H - GAP_Y
draw_box(ax, mx, persp_y, mw, BOX_H,
         "Hospital Perspective\n1-Year Time Horizon",
         edgecolor=COL_MODEL, fontsize=7.5)

# Arrow down
draw_arrow(ax, mx + mw/2, persp_y, mx + mw/2, persp_y - GAP_Y + 0.005)

# Parameters
par_y = persp_y - 0.13 - GAP_Y
draw_box(ax, mx, par_y, mw, 0.13,
         "Cost Parameters\n\nNurse wages | Device costs\nEarly-warning costs\nAdverse-event costs",
         edgecolor=COL_MODEL, fontsize=7)

# Arrow down
draw_arrow(ax, mx + mw/2, par_y, mx + mw/2, par_y - GAP_Y + 0.005)

# Countries
ctr_y = par_y - BOX_H - GAP_Y
draw_box(ax, mx, ctr_y, mw, BOX_H,
         "4 Countries\nJapan | UK | Australia | USA",
         facecolor=COL_MODEL, edgecolor=COL_MODEL,
         fontsize=7.5, fontweight="bold", text_color=WHITE)

# ====================================================================
# SECTION 3 — Analysis
# ====================================================================
ax_x, aw = 0.72, 0.23

analyses = [
    "Cost-Minimization\nAnalysis",
    "Break-Even\nThreshold Analysis",
    "One-Way\nSensitivity Analysis",
    "Multi-Way\nScenario Analysis",
    "Cross-Country\nComparison",
]

top_y = 0.74
step = BOX_H + GAP_Y
for i, label in enumerate(analyses):
    by = top_y - i * step
    fc = COL_ANAL if i == 0 else WHITE
    tc = WHITE if i == 0 else COL_TEXT
    fw = "bold" if i == 0 else "normal"
    draw_box(ax, ax_x, by, aw, BOX_H, label,
             facecolor=fc, edgecolor=COL_ANAL,
             fontsize=7.5, fontweight=fw, text_color=tc)
    if i > 0:
        draw_arrow(ax, ax_x + aw/2, by + BOX_H + GAP_Y - 0.005,
                   ax_x + aw/2, by + BOX_H + 0.005)

# ====================================================================
# Horizontal arrows between sections
# ====================================================================
# Literature → Model (mid-height of the sections)
arr1_y = 0.50
draw_arrow(ax, 0.29 + 0.005, arr1_y, mx - 0.005, arr1_y)

# Model → Analysis
arr2_y = 0.50
draw_arrow(ax, mx + mw + 0.005, arr2_y, 0.695 - 0.005, arr2_y)

# ── Title removed per JCMC convention (figure titles belong in manuscript text only) ─

# ── Save ────────────────────────────────────────────────────────────
fig.tight_layout(pad=0.3)

for ext in ("pdf", "png"):
    fpath = FIGURES / f"fig1_study_overview.{ext}"
    fig.savefig(fpath, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"Saved: {fpath}")

plt.close(fig)
print("Done.")
