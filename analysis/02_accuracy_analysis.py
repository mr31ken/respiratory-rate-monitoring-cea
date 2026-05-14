#!/usr/bin/env python3
"""
02_accuracy_analysis.py
-----------------------
Produce Figure 1: Bland-Altman forest-style plot of all devices.

Outputs:
  ../figures/fig1_accuracy_comparison.pdf
  ../figures/fig1_accuracy_comparison.png
"""

import os, pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import FancyBboxPatch
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["pdf.fonttype"] = 42  # TrueType for journal submission

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────
acc = pd.read_csv(DATA / "accuracy_studies.csv")
dev = pd.read_csv(DATA / "device_characteristics.csv")

# Merge device names and categories
acc_full = acc.merge(dev[["device_id", "device_name", "category"]], on="device_id", how="left")

# ══════════════════════════════════════════════════════════════════════
# Figure 1: Bland-Altman forest-style plot
# ══════════════════════════════════════════════════════════════════════

fig, ax1 = plt.subplots(1, 1, figsize=(8, 7))

# ─────────────────────────────────────────────────────────────────────
# Panel A: Forest-style Bland-Altman plot
# ─────────────────────────────────────────────────────────────────────
# Include all studies that have at least a bias value
ba_data = acc_full.copy()
ba_data["bias_bpm"] = pd.to_numeric(ba_data["bias_bpm"], errors="coerce")
ba_data["loa_lower_bpm"] = pd.to_numeric(ba_data["loa_lower_bpm"], errors="coerce")
ba_data["loa_upper_bpm"] = pd.to_numeric(ba_data["loa_upper_bpm"], errors="coerce")
# Keep rows with at least bias
ba_data = ba_data.dropna(subset=["bias_bpm"]).copy()

# Create label
ba_data["label"] = (ba_data["device_name"].str.replace(r"\s*\(.*?\)", "", regex=True)
                    + "\n" + ba_data["first_author"] + " " + ba_data["year"].astype(str))

# Sort by bias (most negative first)
ba_data = ba_data.sort_values("bias_bpm", ascending=True).reset_index(drop=True)

colors = {
    "Pulse oximetry derived": "#2196F3",
    "Pulse oximetry derived + notification system": "#1565C0",
    "Bedside monitor (impedance)": "#FF9800",
    "Capnography": "#4CAF50",
    "Non-contact (under-mattress)": "#9C27B0",
    "Non-contact (radar)": "#E91E63",
    "Wearable patch": "#00BCD4",
    "Wearable chest belt": "#795548",
}

for i, (_, row) in enumerate(ba_data.iterrows()):
    color = colors.get(row["category"], "#666666")
    has_loa = pd.notna(row["loa_lower_bpm"]) and pd.notna(row["loa_upper_bpm"])

    if has_loa:
        # Full LoA bar
        ax1.barh(i, row["loa_upper_bpm"] - row["loa_lower_bpm"],
                 left=row["loa_lower_bpm"], height=0.55,
                 color=color, alpha=0.25, edgecolor=color, linewidth=1.0)
        # Bias point
        ax1.plot(row["bias_bpm"], i, "o", color=color, markersize=9, zorder=5)
        # Annotation
        annotation = f'Bias {row["bias_bpm"]:.1f}, LoA [{row["loa_lower_bpm"]:.1f}, {row["loa_upper_bpm"]:.1f}]'
        text_x = max(row["loa_upper_bpm"] + 0.3, 3.5)
    else:
        # Bias only (diamond marker)
        ax1.plot(row["bias_bpm"], i, "D", color=color, markersize=8, zorder=5,
                 markeredgecolor="black", markeredgewidth=0.5)
        annotation = f'Bias {row["bias_bpm"]:.1f} (LoA not reported)'
        text_x = row["bias_bpm"] + 0.5

    ax1.text(text_x, i, annotation, va="center", fontsize=7, color=color)

ax1.set_yticks(range(len(ba_data)))
ax1.set_yticklabels(ba_data["label"], fontsize=8)
ax1.axvline(0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
ax1.axvline(-3, color="red", linestyle=":", linewidth=0.8, alpha=0.3)
ax1.axvline(3, color="red", linestyle=":", linewidth=0.8, alpha=0.3)
ax1.set_xlabel("Bias and 95% Limits of Agreement (breaths/min)", fontsize=9)
ax1.set_title("Bland-Altman Agreement with Reference Standards",
              fontsize=10, fontweight="bold", loc="left")
ax1.set_xlim(-10, 12)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Legend for Panel A
from matplotlib.lines import Line2D
legend_a = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="gray", markersize=8,
           label="Bias (with LoA bars)"),
    Line2D([0], [0], marker="D", color="w", markerfacecolor="gray", markersize=7,
           markeredgecolor="black", markeredgewidth=0.5, label="Bias only (LoA N/A)"),
    Line2D([0], [0], color="red", linestyle=":", linewidth=1, label="±3 bpm threshold"),
]
ax1.legend(handles=legend_a, fontsize=7, loc="lower right")


fig.suptitle("Figure 2. Accuracy of Automated Respiratory Rate Monitoring Devices",
             fontsize=12, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(FIGURES / "fig1_accuracy_comparison.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig1_accuracy_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Figure 1 saved to {FIGURES}")
print(f"  {len(ba_data)} studies with bias data")

if __name__ == "__main__":
    print("\n=== 02_accuracy_analysis.py complete ===")
