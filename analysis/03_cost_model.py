#!/usr/bin/env python3
"""
03_cost_model.py
----------------
Deterministic break-even threshold model comparing manual RR counting
with five automated continuous monitoring scenarios.

Model Structure:
  - Comparator: Manual RR counting (standard care)
  - Interventions: 5 device scenarios (see model_core.DEVICES)
  - Perspective: Hospital (direct costs of monitoring); event values are
    reported with their endpoint and cost construct (model_core.event_values)
  - Time horizon: 1 year
  - Cost function and inputs: model_core.py (shared with 04_sensitivity.py)

Outputs:
  ../tables/table3_cost_per_patient_day.csv
  ../tables/table4_breakeven_analysis.csv
  ../figures/fig3_cost.pdf
  ../figures/fig3_cost.png
"""

import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["pdf.fonttype"] = 42

from model_core import (BASE, DEVICES, I_REF, device_components,
                        event_values, breakeven_per_1000, q_required,
                        patient_days_year)

ROOT = pathlib.Path(__file__).resolve().parent.parent
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
TABLES.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

PD_YEAR = patient_days_year()

print("Model base case:")
print(f"  Ward: {BASE['ward_beds']:.0f} beds, occupancy {BASE['occupancy']:.0%}")
print(f"  Patient-days/year: {PD_YEAR:,.0f}")
print(f"  Observations: {BASE['obs_frequency']}/patient-day; "
      f"nurse time released: {BASE['released_sec']:.0f} s/observation")


# ══════════════════════════════════════════════════════════════════════
# Per-patient-day costs (Supplementary Table S2)
# ══════════════════════════════════════════════════════════════════════
rows = []
for name, dev in DEVICES.items():
    c = device_components(name)
    rows.append({
        "scenario": name,
        "category": dev["category"],
        **{k: round(v, 1) for k, v in c.items() if k != "device_staff_min"},
        "device_staff_min_per_pd": c["device_staff_min"],
        "annual_incremental_jpy": round(c["incremental_jpd"] * PD_YEAR),
    })
cost_df = pd.DataFrame(rows)
cost_df.to_csv(TABLES / "table3_cost_per_patient_day.csv", index=False)
print(f"\nTable saved: {TABLES / 'table3_cost_per_patient_day.csv'}")
print(cost_df[["scenario", "gross_device_cost_jpd", "released_manual_time_jpd",
               "incremental_jpd"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# Break-even analysis (main-text Table 3)
# ══════════════════════════════════════════════════════════════════════
ev = event_values()
be_rows = []
for name in DEVICES:
    inc = device_components(name)["incremental_jpd"]
    for ev_name, e in ev.items():
        be = breakeven_per_1000(inc, e["value"])
        q = q_required(be) if e["role"] != "separate" else np.nan
        be_rows.append({
            "device_scenario": name,
            "event_value_scenario": ev_name,
            "role": e["role"],
            "endpoint": e["endpoint"],
            "construct": e["construct"],
            "incremental_cost_jpd": round(inc, 1),
            "event_value_jpy": round(e["value"]),
            "breakeven_events_per_year": round(inc * PD_YEAR / e["value"], 1),
            "breakeven_per_1000pd": round(be, 2),
            "q_required_pct_at_ref_rate": round(q * 100, 1),
            "reference_rate_per_1000pd": I_REF if e["role"] != "separate" else np.nan,
        })
be_df = pd.DataFrame(be_rows)
be_df.to_csv(TABLES / "table4_breakeven_analysis.csv", index=False)
print(f"\nTable saved: {TABLES / 'table4_breakeven_analysis.csv'}")
print({k: round(v["value"]) for k, v in ev.items()})


# ══════════════════════════════════════════════════════════════════════
# Figure 3: Cost components per patient-day (stacked) and released time
# ══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
labels = [DEVICES[n]["short"] for n in cost_df["scenario"]]
x = np.arange(len(labels))
width = 0.6

stack = {
    "capital_jpd": ("#1976D2", "Capital (depreciation)"),
    "maintenance_jpd": ("#42A5F5", "General maintenance"),
    "sensor_replacement_jpd": ("#90CAF9", "Sensor replacement"),
    "consumables_jpd": ("#FF7043", "Consumables"),
    "device_staff_jpd": ("#66BB6A", "Device-related staff time (incl. alarms)"),
}
bottom = np.zeros(len(labels))
for col, (color, label) in stack.items():
    vals = cost_df[col].values
    ax.bar(x, vals, width, bottom=bottom, color=color, label=label,
           edgecolor="white", linewidth=0.5)
    bottom += vals
rel = -cost_df["released_manual_time_jpd"].values
ax.bar(x, rel, width, color="#BDBDBD", label="Released manual-counting time",
       edgecolor="white", linewidth=0.5)
ax.scatter(x, cost_df["incremental_jpd"], marker="D", color="black", zorder=3,
           s=28, label="Incremental cost (ΔC)")
for i, (g, inc) in enumerate(zip(cost_df["gross_device_cost_jpd"],
                                  cost_df["incremental_jpd"])):
    ax.text(i, g + 25, f"ΔC ¥{inc:,.0f}", ha="center", fontsize=8,
            fontweight="bold")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel("JPY per patient-day", fontsize=10)
ax.set_ylim(rel.min() * 1.6, cost_df["gross_device_cost_jpd"].max() * 1.15)
ax.legend(fontsize=8, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(0.02, -0.12,
        f"Japan base case: {BASE['ward_beds']:.0f}-bed ward, "
        f"{BASE['occupancy']:.0%} occupancy, nurse ¥{BASE['nurse_hourly']:,.0f}/h, "
        f"{BASE['obs_frequency']} observations/patient-day, "
        f"{BASE['released_sec']:.0f} s released per observation. "
        "Inputs: data/cost_parameters.csv and analysis/model_core.py.",
        transform=ax.transAxes, fontsize=7, color="gray", wrap=True)
plt.tight_layout()
fig.savefig(FIGURES / "fig3_cost.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig3_cost.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"\nFigure 3 saved to {FIGURES}")

if __name__ == "__main__":
    print("\n=== 03_cost_model.py complete ===")
