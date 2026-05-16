#!/usr/bin/env python3
"""
04_sensitivity.py
-----------------
One-way sensitivity analysis and break-even visualization.

Outputs:
  ../figures/fig4_breakeven.pdf
  ../figures/fig4_breakeven.png
  ../figures/fig5_tornado.pdf
  ../figures/fig5_tornado.png
  ../figures/fig6_scenario.pdf
  ../figures/fig6_scenario.png
  ../tables/table5_sensitivity.csv
"""

import os, pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["pdf.fonttype"] = 42

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
TABLES.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

params = pd.read_csv(DATA / "cost_parameters.csv")

def get_param(pid):
    row = params[params["parameter_id"] == pid]
    return float(row["value"].iloc[0])

# ══════════════════════════════════════════════════════════════════════
# Base-case parameters (Japan)
# ══════════════════════════════════════════════════════════════════════
BASE = {
    "nurse_hourly": get_param("COST_JP03"),         # 3500 JPY
    "obs_time_sec": get_param("MODEL01"),            # 80 s
    "obs_frequency": get_param("MODEL02"),           # 4.5/day
    "occupancy": get_param("MODEL04"),               # 0.90
    "ward_beds": get_param("MODEL03"),               # 30
    "device_life": get_param("MODEL05"),             # 7 yr
    "maint_rate": get_param("MODEL07"),              # 0.08
    "device_cost_per_bed": 665000,                   # EarlySense-type in JPY
    "sensor_replace_annual": 475 * get_param("FX02"),# annual sensor cost JPY
    "consumable_pd": 0,
    "staff_min_device": 3,                           # min/patient-day for device
    "ae_cost": (get_param("COST_JP02") * 3 + get_param("COST_JP01") * 5),
}

def compute_incremental(p):
    """Compute incremental cost/patient-day of device vs manual (JPY)."""
    pd_per_bed = p["occupancy"] * 365

    # Manual cost
    manual_pd = (p["nurse_hourly"] * p["obs_time_sec"] / 3600) * p["obs_frequency"]

    # Device cost
    device_annual = p["device_cost_per_bed"] / p["device_life"]
    maint_annual = p["device_cost_per_bed"] * p["maint_rate"] + p["sensor_replace_annual"]
    device_pd = (device_annual + maint_annual) / pd_per_bed
    consumable = p["consumable_pd"]
    staff_device = (p["staff_min_device"] / 60) * p["nurse_hourly"]
    device_total = device_pd + consumable + staff_device

    incremental = device_total - manual_pd
    return incremental

def compute_breakeven_events(incremental, ae_cost, patient_days_year):
    """Break-even adverse events per year."""
    if ae_cost <= 0:
        return float("inf")
    return (incremental * patient_days_year) / ae_cost

base_inc = compute_incremental(BASE)
base_pd_year = BASE["ward_beds"] * BASE["occupancy"] * 365
base_be = compute_breakeven_events(base_inc, BASE["ae_cost"], base_pd_year)

print(f"Base case incremental cost: ¥{base_inc:,.1f}/patient-day")
print(f"Base case break-even: {base_be:.1f} events/year")


# ══════════════════════════════════════════════════════════════════════
# One-Way Sensitivity Analysis
# ══════════════════════════════════════════════════════════════════════
sensitivity_ranges = {
    "Nurse hourly cost (JPY)": ("nurse_hourly", 2800, 4200),
    "Manual obs time (sec)": ("obs_time_sec", 60, 120),
    "Monitoring frequency (obs/day)": ("obs_frequency", 2, 8),
    "Ward occupancy": ("occupancy", 0.75, 0.95),
    "Device cost/bed (JPY)": ("device_cost_per_bed", 400000, 1000000),
    "Device useful life (yr)": ("device_life", 5, 10),
    "Maintenance rate (%)": ("maint_rate", 0.05, 0.12),
    "Staff time for device (min/pd)": ("staff_min_device", 1, 8),
    "Adverse event cost (JPY)": ("ae_cost", 300000, 2000000),
}

tornado_data = []
sensitivity_rows = []
for label, (key, low, high) in sensitivity_ranges.items():
    # Low value
    p_low = BASE.copy()
    p_low[key] = low
    inc_low = compute_incremental(p_low)
    pd_year_low = p_low["ward_beds"] * p_low["occupancy"] * 365
    ae_low = p_low["ae_cost"]
    be_low = compute_breakeven_events(inc_low, ae_low, pd_year_low)

    # High value
    p_high = BASE.copy()
    p_high[key] = high
    inc_high = compute_incremental(p_high)
    pd_year_high = p_high["ward_beds"] * p_high["occupancy"] * 365
    ae_high = p_high["ae_cost"]
    be_high = compute_breakeven_events(inc_high, ae_high, pd_year_high)

    tornado_data.append({
        "parameter": label,
        "low_value": low,
        "high_value": high,
        "be_at_low": be_low,
        "be_at_high": be_high,
        "range": abs(be_high - be_low)
    })

    sensitivity_rows.append({
        "parameter": label,
        "base_value": BASE[key],
        "low_value": low,
        "high_value": high,
        "incremental_at_low": round(inc_low, 1),
        "incremental_at_high": round(inc_high, 1),
        "breakeven_at_low": round(be_low, 1),
        "breakeven_at_high": round(be_high, 1),
        "base_incremental": round(base_inc, 1),
        "base_breakeven": round(base_be, 1)
    })

sens_df = pd.DataFrame(sensitivity_rows)
sens_df.to_csv(TABLES / "table5_sensitivity.csv", index=False)
print(f"\nTable 5 saved: {TABLES / 'table5_sensitivity.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Figure 4: Break-even Analysis (multi-country)
# ══════════════════════════════════════════════════════════════════════
# For each device type, show break-even events using different country AE costs
device_types = {
    "Under-mattress\n(EarlySense-type)": {"inc_jpd": None},  # filled from table3
    "Bedside monitor\n(impedance)": {"inc_jpd": None},
    "Capnography\n(Capnostream-type)": {"inc_jpd": None},
    "Wearable patch\n(RespiraSense-type)": {"inc_jpd": None},
    "Radar sensor\n(Guardian M10-type)": {"inc_jpd": None},
}

# Load table3 for incremental costs
try:
    t3 = pd.read_csv(TABLES / "table3_cost_per_patient_day.csv")
    mapping = {
        "Under-mattress sensor (EarlySense-type)": "Under-mattress\n(EarlySense-type)",
        "Bedside monitor (impedance RR)": "Bedside monitor\n(impedance)",
        "Capnography (Capnostream-type)": "Capnography\n(Capnostream-type)",
        "Wearable patch (RespiraSense-type)": "Wearable patch\n(RespiraSense-type)",
        "Radar sensor (Guardian M10-type)": "Radar sensor\n(Guardian M10-type)"
    }
    for t3_name, fig_name in mapping.items():
        row = t3[t3["scenario"] == t3_name]
        if not row.empty:
            device_types[fig_name]["inc_jpd"] = row["incremental_vs_manual_jpd"].iloc[0]
except Exception as e:
    print(f"Warning: Could not load table3: {e}")
    # Use base-case estimate for all
    for k in device_types:
        device_types[k]["inc_jpd"] = base_inc

FX_GBP_JPY = get_param("FX02")
FX_AUD_JPY = get_param("FX04")
FX_USD_JPY = get_param("FX01")

country_ae_costs_jpy = {
    "Japan\n(bed-day)": get_param("COST_JP02") * 3 + get_param("COST_JP01") * 5,
    "Japan\n(w/ procedures)": 1_000_000,
    "UK\n(2020-21 NCC)": (1881 * 3 + 345 * 5) * FX_GBP_JPY,
    "Australia\n(Curtis 2021)": 14134 * FX_AUD_JPY,
    "USA\n(Blike 2025)": 10700 * FX_USD_JPY,
}

fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(device_types))
n_countries = len(country_ae_costs_jpy)
bar_width = 0.15
country_colors = ["#1565C0", "#42A5F5", "#E65100", "#66BB6A", "#AB47BC"]

for i, (country, ae_cost) in enumerate(country_ae_costs_jpy.items()):
    be_values = []
    for dev_name, dev_data in device_types.items():
        inc = dev_data["inc_jpd"]
        if inc is not None and inc > 0:
            be = (inc / ae_cost) * 1000  # per 1000 patient-days
        else:
            be = 0
        be_values.append(be)

    offset = (i - n_countries / 2 + 0.5) * bar_width
    ax.bar(x + offset, be_values, bar_width, label=country.replace("\n", " "),
           color=country_colors[i], alpha=0.85, edgecolor="white", linewidth=0.5)

ax.set_xticks(x)
ax.set_xticklabels([k.replace("\n", "\n") for k in device_types.keys()],
                   fontsize=8, ha="center")
ax.set_ylabel("Break-even: adverse events avoided\n(per 1,000 patient-days)", fontsize=9)
# Title removed per JCMC requirements (no chart titles inside figures)
ax.legend(fontsize=7, loc="upper right", ncol=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ward_beds = int(BASE["ward_beds"])
occupancy = BASE["occupancy"]
ax.text(0.02, -0.15,
        f"Base case: {ward_beds}-bed ward, {occupancy:.0%} occupancy. "
        "Values represent the minimum number of deterioration events that must be "
        "avoided per 1,000 patient-days for the monitoring investment to break even.",
        transform=ax.transAxes, fontsize=7, color="gray", wrap=True)

plt.tight_layout()
fig.savefig(FIGURES / "fig4_breakeven.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig4_breakeven.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"\nFigure 4 saved to {FIGURES}")


# ══════════════════════════════════════════════════════════════════════
# Figure 5: Tornado Diagram
# ══════════════════════════════════════════════════════════════════════
tornado_df = pd.DataFrame(tornado_data).sort_values("range", ascending=True)

# Increased height ~30% (6 -> 7.8) to reduce vertical crowding of labels
fig, ax = plt.subplots(figsize=(9, 7.8))

y = np.arange(len(tornado_df))
# Compute x-range to position outside-bar labels with a small offset
x_min_data = min(tornado_df["be_at_low"].min(), tornado_df["be_at_high"].min())
x_max_data = max(tornado_df["be_at_low"].max(), tornado_df["be_at_high"].max())
x_span = x_max_data - x_min_data
label_offset = x_span * 0.015

for i, (_, row) in enumerate(tornado_df.iterrows()):
    low_val = min(row["be_at_low"], row["be_at_high"])
    high_val = max(row["be_at_low"], row["be_at_high"])

    # Bar from low to base
    ax.barh(i, base_be - low_val, left=low_val, height=0.6,
            color="#1976D2", alpha=0.7)
    # Bar from base to high
    ax.barh(i, high_val - base_be, left=base_be, height=0.6,
            color="#E53935", alpha=0.7)

    # Labels — placed OUTSIDE the bars (past the bar edge) to avoid overlap
    ax.text(low_val - label_offset, i, f'{row["low_value"]}',
            ha="right", va="center", fontsize=7, color="#1976D2")
    ax.text(high_val + label_offset, i, f'{row["high_value"]}',
            ha="left", va="center", fontsize=7, color="#E53935")

ax.axvline(base_be, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
ax.set_yticks(y)
# Slightly smaller font for y-tick labels to reduce overlap with bar values
ax.set_yticklabels(tornado_df["parameter"], fontsize=8)
ax.set_xlabel("Break-even: adverse events avoided per year", fontsize=10)
# Title removed per JCMC requirements (no chart titles inside figures)

# Extend x-limits so the outside-bar value labels are not clipped
ax.set_xlim(x_min_data - x_span * 0.10, x_max_data + x_span * 0.10)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor="#1976D2", alpha=0.7, label="Low parameter value"),
                   Patch(facecolor="#E53935", alpha=0.7, label="High parameter value")]
ax.legend(handles=legend_elements, fontsize=8, loc="lower right")

ax.text(0.02, -0.08,
        f"Vertical dashed line: base-case break-even ({base_be:.1f} events/year). "
        "Numbers at bar ends show parameter values tested.",
        transform=ax.transAxes, fontsize=7, color="gray")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# Increase left margin so long y-axis parameter labels (e.g. "Adverse event cost (¥)")
# are not clipped; also give a bit of bottom room for the caption text.
plt.subplots_adjust(left=0.28, right=0.96, top=0.95, bottom=0.15)
fig.savefig(FIGURES / "fig5_tornado.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig5_tornado.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"\nFigure 5 saved to {FIGURES}")

# ══════════════════════════════════════════════════════════════════════
# Multi-Way Scenario Analysis (Best / Base / Worst)
# ══════════════════════════════════════════════════════════════════════
# Simultaneously vary ALL assumption parameters to produce
# best-case, base-case, and worst-case break-even thresholds.

scenarios = {
    "Best case\n(device favored)": {
        "nurse_hourly": 4200,        # high → manual more expensive
        "obs_time_sec": 120,         # long manual obs → more expensive
        "obs_frequency": 6,          # high frequency → more manual cost
        "occupancy": 0.95,           # high occupancy → more patient-days to amortize
        "device_cost_per_bed": 400000,  # cheap device
        "device_life": 10,           # long life
        "maint_rate": 0.05,          # low maintenance
        "staff_min_device": 1,       # minimal device staff time
        "ae_cost": 2_000_000,        # high AE cost → fewer events needed
        "ward_beds": BASE["ward_beds"],
        "sensor_replace_annual": BASE["sensor_replace_annual"],
        "consumable_pd": BASE["consumable_pd"],
    },
    "Base case": {k: v for k, v in BASE.items()},
    "Worst case\n(device disfavored)": {
        "nurse_hourly": 2800,        # low → manual cheaper
        "obs_time_sec": 60,          # quick manual obs
        "obs_frequency": 2,          # low frequency → low manual cost
        "occupancy": 0.75,           # low occupancy → fewer pt-days to amortize
        "device_cost_per_bed": 1000000,  # expensive device
        "device_life": 5,            # short life
        "maint_rate": 0.12,          # high maintenance
        "staff_min_device": 8,       # high device staff time
        "ae_cost": 300_000,          # low AE cost → many events needed
        "ward_beds": BASE["ward_beds"],
        "sensor_replace_annual": BASE["sensor_replace_annual"],
        "consumable_pd": BASE["consumable_pd"],
    },
}

scenario_results = []
for sc_name, sc_params in scenarios.items():
    inc = compute_incremental(sc_params)
    pd_year = sc_params["ward_beds"] * sc_params["occupancy"] * 365
    ae = sc_params["ae_cost"]
    be = compute_breakeven_events(inc, ae, pd_year)
    be_per_1000 = (inc / ae) * 1000 if ae > 0 else float("inf")

    scenario_results.append({
        "scenario": sc_name.replace("\n", " "),
        "incremental_cost_jpd": round(inc, 1),
        "ae_cost_jpy": round(ae),
        "breakeven_events_year": round(be, 1),
        "breakeven_per_1000pd": round(be_per_1000, 2),
    })

scenario_df = pd.DataFrame(scenario_results)
scenario_df.to_csv(TABLES / "table6_scenario_analysis.csv", index=False)
print(f"\nTable 6 (scenario analysis) saved: {TABLES / 'table6_scenario_analysis.csv'}")
print(scenario_df.to_string(index=False))

# ── Figure 6: Scenario comparison bar chart ──────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

sc_labels = [s.replace("\n", " ") for s in scenarios.keys()]
be_values = [r["breakeven_per_1000pd"] for r in scenario_results]
colors_sc = ["#4CAF50", "#2196F3", "#E53935"]

bars = ax.bar(range(len(sc_labels)), be_values, color=colors_sc, width=0.5,
              edgecolor="white", linewidth=1.5)

for i, (bar, val) in enumerate(zip(bars, be_values)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

ax.set_xticks(range(len(sc_labels)))
ax.set_xticklabels(sc_labels, fontsize=10)
ax.set_ylabel("Break-even: adverse events avoided\n(per 1,000 patient-days)", fontsize=10)
# Title removed per JCMC requirements (no chart titles inside figures)

# Reference line: typical deterioration rate range
ax.axhline(y=2, color="orange", linestyle="--", linewidth=1, alpha=0.7)
ax.axhline(y=10, color="orange", linestyle="--", linewidth=1, alpha=0.7)
ax.text(len(sc_labels) - 0.6, 2.2, "Lower bound: typical\ndeterioration rate",
        fontsize=7, color="orange", alpha=0.8)
ax.text(len(sc_labels) - 0.6, 10.2, "Upper bound: typical\ndeterioration rate",
        fontsize=7, color="orange", alpha=0.8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.text(0.02, -0.15,
        "Best case: all assumption parameters simultaneously set to values favoring device adoption.\n"
        "Worst case: all assumption parameters simultaneously set to values disfavoring device adoption.\n"
        "Orange dashed lines: published range of deterioration events (2–10 per 1,000 patient-days [17, 21]).",
        transform=ax.transAxes, fontsize=7, color="gray")

plt.tight_layout()
fig.savefig(FIGURES / "fig6_scenario.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig6_scenario.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"\nFigure 6 saved to {FIGURES}")

if __name__ == "__main__":
    print("\n=== 04_sensitivity.py complete ===")
