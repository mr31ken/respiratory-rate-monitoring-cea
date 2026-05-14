#!/usr/bin/env python3
"""
03_cost_model.py
----------------
Deterministic cost-effectiveness model comparing manual RR measurement
with automated continuous monitoring devices.

Model Structure:
  - Comparator: Manual RR counting (standard care)
  - Interventions: 5 device categories (see data/device_characteristics.csv)
  - Perspective: Hospital (direct costs)
  - Time horizon: 1 year
  - Countries: Japan, UK, Australia, USA

Outputs:
  ../tables/table3_cost_per_patient_day.csv
  ../tables/table4_breakeven_analysis.csv
  ../figures/fig2_cost_comparison.pdf
  ../figures/fig2_cost_comparison.png
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

# ══════════════════════════════════════════════════════════════════════
# Load parameters
# ══════════════════════════════════════════════════════════════════════
params = pd.read_csv(DATA / "cost_parameters.csv")

def get_param(pid):
    """Get parameter value by parameter_id."""
    row = params[params["parameter_id"] == pid]
    if row.empty:
        raise ValueError(f"Parameter {pid} not found")
    return float(row["value"].iloc[0])

# ── Model Parameters ─────────────────────────────────────────────────
WARD_BEDS = int(get_param("MODEL03"))
OCCUPANCY = get_param("MODEL04")
FREQ_STANDARD = get_param("MODEL02")   # observations per patient-day
TIME_PER_OBS_SEC = get_param("MODEL01")  # seconds per manual observation
DEVICE_LIFE_MONITOR = int(get_param("MODEL05"))
DEVICE_LIFE_WEARABLE = int(get_param("MODEL06"))
MAINT_RATE = get_param("MODEL07")

# Exchange rates (for cross-country reference)
FX_USD_JPY = get_param("FX01")
FX_GBP_JPY = get_param("FX02")
FX_EUR_JPY = get_param("FX03")
FX_AUD_JPY = get_param("FX04")

# Derived
PATIENT_DAYS_YEAR = WARD_BEDS * OCCUPANCY * 365
TIME_PER_OBS_HOURS = TIME_PER_OBS_SEC / 3600

print(f"Model base case:")
print(f"  Ward: {WARD_BEDS} beds, occupancy {OCCUPANCY:.0%}")
print(f"  Patient-days/year: {PATIENT_DAYS_YEAR:,.0f}")
print(f"  Standard monitoring: {FREQ_STANDARD} obs/patient-day")
print(f"  Manual RR time: {TIME_PER_OBS_SEC}s/obs")


# ══════════════════════════════════════════════════════════════════════
# Japan-specific Cost Model
# ══════════════════════════════════════════════════════════════════════
NURSE_HOURLY_JP = get_param("COST_JP03")
WARD_COST_JP = get_param("COST_JP01")
ICU_COST_JP = get_param("COST_JP02")

# ── Manual RR cost (Japan) ───────────────────────────────────────────
manual_cost_per_obs_jp = NURSE_HOURLY_JP * TIME_PER_OBS_HOURS
manual_cost_per_pd_jp = manual_cost_per_obs_jp * FREQ_STANDARD

# ── Device costs (Japan, JPY) ────────────────────────────────────────
# Define device scenarios with explicit cost assumptions
device_scenarios_jp = {
    "Manual (standard care)": {
        "device_cost_per_bed": 0,
        "useful_life": 1,
        "annual_maint": 0,
        "consumable_per_pd": 0,
        "staff_time_min_per_pd": FREQ_STANDARD * TIME_PER_OBS_SEC / 60,
        "category": "Manual"
    },
    "Under-mattress sensor\n(EarlySense-type)": {
        "device_cost_per_bed": 35000 * FX_GBP_JPY / 10,  # £35000/10 beds
        "useful_life": DEVICE_LIFE_MONITOR,
        "annual_maint": 475 * FX_GBP_JPY,  # £475/bed/year sensor replacement
        "consumable_per_pd": 0,
        "staff_time_min_per_pd": 3,  # alarm management
        "category": "Non-contact"
    },
    "Bedside monitor\n(impedance RR)": {
        "device_cost_per_bed": 1_350_000,  # PVM-4000 ¥1,350,000
        "useful_life": DEVICE_LIFE_MONITOR,
        "annual_maint": 1_350_000 * MAINT_RATE,
        "consumable_per_pd": 200,  # ECG electrodes ~¥200/day
        "staff_time_min_per_pd": 4,  # electrode change + alarm mgmt
        "category": "Impedance"
    },
    "Capnography\n(Capnostream-type)": {
        "device_cost_per_bed": 4500 * FX_USD_JPY,  # mid-range $4500
        "useful_life": DEVICE_LIFE_MONITOR,
        "annual_maint": 4500 * FX_USD_JPY * MAINT_RATE,
        "consumable_per_pd": 10 * FX_USD_JPY,  # FilterLine ~$10/day
        "staff_time_min_per_pd": 5,  # line change + alarm mgmt
        "category": "Capnography"
    },
    "Wearable patch\n(RespiraSense-type)": {
        "device_cost_per_bed": 0,  # patch-based, no capital per bed
        "useful_life": DEVICE_LIFE_WEARABLE,
        "annual_maint": 0,
        "consumable_per_pd": 35 * FX_GBP_JPY / 7,  # £35/patch lasting ~7 days
        "staff_time_min_per_pd": 5,  # application + checking
        "category": "Wearable"
    },
    "Radar sensor\n(Guardian M10-type)": {
        "device_cost_per_bed": 500_000,  # estimated (not public; conservative)
        "useful_life": DEVICE_LIFE_MONITOR,
        "annual_maint": 500_000 * MAINT_RATE,
        "consumable_per_pd": 0,
        "staff_time_min_per_pd": 2,  # minimal (non-contact)
        "category": "Non-contact"
    }
}

# ── Calculate costs per patient-day ──────────────────────────────────
results = []
for name, sc in device_scenarios_jp.items():
    # Annualized device cost per bed
    if sc["device_cost_per_bed"] > 0:
        annual_device = sc["device_cost_per_bed"] / sc["useful_life"]
    else:
        annual_device = 0
    annual_maint = sc["annual_maint"]

    # Per patient-day
    patient_days_per_bed = OCCUPANCY * 365
    device_pd = (annual_device + annual_maint) / patient_days_per_bed
    consumable_pd = sc["consumable_per_pd"]
    staff_pd = (sc["staff_time_min_per_pd"] / 60) * NURSE_HOURLY_JP

    total_pd = device_pd + consumable_pd + staff_pd

    results.append({
        "scenario": name.replace("\n", " "),
        "category": sc["category"],
        "device_depreciation_jpd": round(device_pd, 1),
        "maintenance_jpd": round(annual_maint / patient_days_per_bed, 1),
        "consumables_jpd": round(consumable_pd, 1),
        "staff_time_jpd": round(staff_pd, 1),
        "total_cost_jpd": round(total_pd, 1),
        "incremental_vs_manual_jpd": round(total_pd - manual_cost_per_pd_jp, 1),
        "annual_total_jpy": round(total_pd * PATIENT_DAYS_YEAR),
        "staff_minutes_per_pd": sc["staff_time_min_per_pd"]
    })

cost_df = pd.DataFrame(results)
cost_df.to_csv(TABLES / "table3_cost_per_patient_day.csv", index=False)
print(f"\nTable 3 saved: {TABLES / 'table3_cost_per_patient_day.csv'}")
print(cost_df[["scenario", "total_cost_jpd", "incremental_vs_manual_jpd"]].to_string(index=False))


# ══════════════════════════════════════════════════════════════════════
# Break-even Analysis
# ══════════════════════════════════════════════════════════════════════
# How many adverse events must be avoided to offset device cost?

adverse_event_costs = {
    "Japan (bed-day estimate)": {
        "cost_per_event": (ICU_COST_JP * 3 + WARD_COST_JP * 5),  # 3 ICU + 5 ward days
        "currency": "JPY",
        "note": "3 additional ICU days + 5 additional ward days (lower bound)"
    },
    "Japan (with procedures)": {
        "cost_per_event": 1_000_000,
        "currency": "JPY",
        "note": "Sensitivity estimate including procedures/drugs"
    },
    "UK (2020-21 NCC)": {
        "cost_per_event": (1881 * 3 + 345 * 5) * FX_GBP_JPY,
        "currency": "JPY (converted)",
        "note": f"£{1881*3+345*5:,.0f} converted at ¥{FX_GBP_JPY}/£ (2020/21 NCC via Parliament WQ 165361)"
    },
    "Australia (Curtis 2021)": {
        "cost_per_event": 14134 * FX_AUD_JPY,
        "currency": "JPY (converted)",
        "note": f"A$14,134 converted at ¥{FX_AUD_JPY}/A$"
    },
    "USA (Blike 2025 transfer)": {
        "cost_per_event": 10700 * FX_USD_JPY,
        "currency": "JPY (converted)",
        "note": f"$10,700 operating margin impact per transfer avoided"
    }
}

breakeven_rows = []
for dev_name, dev_data in device_scenarios_jp.items():
    if dev_data["category"] == "Manual":
        continue
    dev_clean = dev_name.replace("\n", " ")
    # Get incremental cost
    inc = cost_df[cost_df["scenario"] == dev_clean]["incremental_vs_manual_jpd"].iloc[0]

    for ae_name, ae_data in adverse_event_costs.items():
        ae_cost = ae_data["cost_per_event"]
        # Break-even: inc_cost * patient_days = n_events * ae_cost
        # n_events = inc_cost * patient_days / ae_cost
        events_per_year = (inc * PATIENT_DAYS_YEAR) / ae_cost if ae_cost > 0 else float("inf")
        events_per_1000pd = (inc / ae_cost) * 1000 if ae_cost > 0 else float("inf")

        breakeven_rows.append({
            "device_scenario": dev_clean,
            "adverse_event_cost_scenario": ae_name,
            "incremental_cost_jpd": inc,
            "adverse_event_cost_jpy": round(ae_cost),
            "breakeven_events_per_year": round(events_per_year, 1),
            "breakeven_per_1000pd": round(events_per_1000pd, 2),
            "note": ae_data["note"]
        })

be_df = pd.DataFrame(breakeven_rows)
be_df.to_csv(TABLES / "table4_breakeven_analysis.csv", index=False)
print(f"\nTable 4 saved: {TABLES / 'table4_breakeven_analysis.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Figure 2: Cost Comparison (stacked bar)
# ══════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))

categories = cost_df["scenario"].tolist()
x = np.arange(len(categories))
width = 0.6

colors_stack = {
    "device_depreciation_jpd": ("#1976D2", "Device depreciation"),
    "maintenance_jpd": ("#42A5F5", "Maintenance"),
    "consumables_jpd": ("#FF7043", "Consumables"),
    "staff_time_jpd": ("#66BB6A", "Staff time"),
}

bottom = np.zeros(len(categories))
for col, (color, label) in colors_stack.items():
    values = cost_df[col].values
    ax.bar(x, values, width, bottom=bottom, color=color, label=label, edgecolor="white", linewidth=0.5)
    bottom += values

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8, rotation=15, ha="right")
ax.set_ylabel("Cost per patient-day (JPY)", fontsize=10)
ax.set_title("Figure 3. Per-Patient-Day Cost Comparison:\n"
             "Manual RR Measurement vs. Automated Monitoring Devices",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8, loc="upper left")

# Add total cost labels
for i, total in enumerate(cost_df["total_cost_jpd"]):
    ax.text(i, total + 20, f"¥{total:,.0f}", ha="center", fontsize=8, fontweight="bold")

ax.set_ylim(0, cost_df["total_cost_jpd"].max() * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Base case note
ax.text(0.02, -0.18,
        f"Base case: {WARD_BEDS}-bed ward, {OCCUPANCY:.0%} occupancy, "
        f"{FREQ_STANDARD} obs/day (manual), nurse ¥{NURSE_HOURLY_JP:,.0f}/hr. "
        f"All assumptions in data/cost_parameters.csv.",
        transform=ax.transAxes, fontsize=7, color="gray", wrap=True)

plt.tight_layout()
fig.savefig(FIGURES / "fig2_cost_comparison.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig2_cost_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"\nFigure 2 saved to {FIGURES}")

if __name__ == "__main__":
    print("\n=== 03_cost_model.py complete ===")
