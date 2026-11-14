#!/usr/bin/env python3
"""
04_sensitivity.py
-----------------
Break-even visualisation, one-way sensitivity, released-time and
alarm-burden scenarios, two-way threshold analysis, required avoidable
fraction, and an all-extremes stress test. Uses the same cost function as
03_cost_model.py (model_core.py).

Outputs:
  ../figures/fig4_breakeven.pdf / .png
  ../figures/fig5_tornado.pdf / .png
  ../figures/fig6_required_fraction.pdf / .png
  ../tables/table5_sensitivity.csv
  ../tables/table6_scenario_analysis.csv
  ../tables/table7_two_way.csv
  ../tables/table8_stress_test.csv
"""

import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["pdf.fonttype"] = 42

from model_core import (BASE, DEVICES, REPRESENTATIVE, I_REF, FULL_COUNT_SEC,
                        device_components, incremental, device_price_jpy,
                        event_values, breakeven_per_1000, q_required)

ROOT = pathlib.Path(__file__).resolve().parent.parent
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
TABLES.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

EV = event_values()
B_JP = EV["Japan, fee schedule"]["value"]
B_JP_CLAIMS = EV["Japan, claims-based ICU charges"]["value"]
B_UK = EV["UK, NHS cost collection"]["value"]
REP = REPRESENTATIVE
REP_PRICE = device_price_jpy(DEVICES[REP], BASE)

base_inc = incremental(REP)
base_be = breakeven_per_1000(base_inc, B_JP)
print(f"Representative device: {REP}")
print(f"  Incremental cost: ¥{base_inc:,.1f}/patient-day")
print(f"  Break-even (Japan, fee schedule): {base_be:.2f}/1,000 patient-days; "
      f"q_required at I={I_REF}: {q_required(base_be):.1%}")


def evaluate(p, b=B_JP, name=REP, staff_min=None):
    inc = incremental(name, p, staff_min)
    be = breakeven_per_1000(inc, b)
    return inc, be


# ══════════════════════════════════════════════════════════════════════
# One-way sensitivity (representative device, Japan fee-schedule B)
# ══════════════════════════════════════════════════════════════════════
# (label, key, low, high, kind)
ONE_WAY = [
    ("Nurse hourly cost (JPY)", "nurse_hourly", 2800, 4200, "p"),
    ("Nurse time released per observation (s)", "released_sec", 0,
     FULL_COUNT_SEC, "p"),
    ("Monitoring frequency (obs/day)", "obs_frequency", 2, 8, "p"),
    ("Ward occupancy", "occupancy", 0.75, 0.95, "p"),
    ("Device price per bed (JPY)", "price", 400_000, 1_000_000, "price"),
    ("Device useful life (yr)", "life_monitor", 5, 10, "p"),
    ("General maintenance rate", "maint_rate", 0.05, 0.12, "p"),
    ("Device-related staff time incl. alarms (min/pd)", "staff", 1, 8, "staff"),
    ("GBP/JPY exchange rate (±15%)", "fx_gbp", BASE["fx_gbp"] * 0.85,
     BASE["fx_gbp"] * 1.15, "p"),
    ("Event value, Japan (fee schedule → claims-based ICU charges)", "b",
     B_JP, B_JP_CLAIMS, "b"),
]


def run_one(key, val, kind):
    p = BASE.copy()
    b, staff = B_JP, None
    if kind == "p":
        p[key] = val
    elif kind == "price":
        p["price_scale"] = val / REP_PRICE
    elif kind == "staff":
        staff = val
    elif kind == "b":
        b = val
    return evaluate(p, b, staff_min=staff)


sens_rows = []
for label, key, low, high, kind in ONE_WAY:
    inc_lo, be_lo = run_one(key, low, kind)
    inc_hi, be_hi = run_one(key, high, kind)
    base_val = {"price": REP_PRICE, "staff": DEVICES[REP]["staff_min"],
                "b": B_JP}.get(kind, BASE.get(key))
    sens_rows.append({
        "parameter": label, "base_value": round(base_val, 3),
        "low_value": round(low, 3), "high_value": round(high, 3),
        "incremental_at_low": round(inc_lo, 1),
        "incremental_at_high": round(inc_hi, 1),
        "breakeven_per_1000pd_at_low": round(be_lo, 2),
        "breakeven_per_1000pd_at_high": round(be_hi, 2),
        "q_required_pct_at_low": round(q_required(be_lo) * 100, 1),
        "q_required_pct_at_high": round(q_required(be_hi) * 100, 1),
        "base_incremental": round(base_inc, 1),
        "base_breakeven_per_1000pd": round(base_be, 2),
        "range": abs(be_hi - be_lo),
    })
sens_df = pd.DataFrame(sens_rows)
sens_df.drop(columns="range").to_csv(TABLES / "table5_sensitivity.csv",
                                     index=False)
print(f"\nTable 5 saved: {TABLES / 'table5_sensitivity.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Figure 4: Break-even by device and event value (ICU-transfer endpoint)
# ══════════════════════════════════════════════════════════════════════
fig_ev = [k for k, e in EV.items() if e["role"] != "separate"]
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(DEVICES))
bw = 0.25
colors = ["#1565C0", "#E65100", "#90CAF9"]
for i, ev_name in enumerate(fig_ev):
    vals = [breakeven_per_1000(incremental(n), EV[ev_name]["value"])
            for n in DEVICES]
    lab = ev_name + (" (variant)" if EV[ev_name]["role"] == "variant" else "")
    ax.bar(x + (i - 1) * bw, vals, bw, label=lab, color=colors[i],
           edgecolor="white", linewidth=0.5)
ax.set_xticks(x)
ax.set_xticklabels([DEVICES[n]["short"] for n in DEVICES], fontsize=9)
ax.set_ylabel("Break-even: unplanned ICU transfers averted\n"
              "per 1,000 patient-days", fontsize=9)
ax.legend(fontsize=8, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(0.02, -0.13,
        "Values are thresholds (events that must be averted), not event rates. "
        "Australian and US values use a different endpoint or construct and "
        "are reported separately (Table 3).",
        transform=ax.transAxes, fontsize=7, color="gray", wrap=True)
plt.tight_layout()
fig.savefig(FIGURES / "fig4_breakeven.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig4_breakeven.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Figure 4 saved to {FIGURES}")


# ══════════════════════════════════════════════════════════════════════
# Figure 5: Tornado (representative device, Japan fee-schedule B)
# ══════════════════════════════════════════════════════════════════════
tdf = sens_df.sort_values("range", ascending=True).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(9, 7.8))
lo_all = tdf[["breakeven_per_1000pd_at_low", "breakeven_per_1000pd_at_high"]].min(axis=1)
hi_all = tdf[["breakeven_per_1000pd_at_low", "breakeven_per_1000pd_at_high"]].max(axis=1)
span = hi_all.max() - lo_all.min()
off = span * 0.015


def fmt(v):
    return f"{v:,.0f}" if abs(v) >= 100 else (f"{v:g}")


for i, r in tdf.iterrows():
    lo_be, hi_be = r["breakeven_per_1000pd_at_low"], r["breakeven_per_1000pd_at_high"]
    left, right = min(lo_be, hi_be), max(lo_be, hi_be)
    lo_lab = r["low_value"] if lo_be <= hi_be else r["high_value"]
    hi_lab = r["high_value"] if lo_be <= hi_be else r["low_value"]
    ax.barh(i, base_be - left, left=left, height=0.6, color="#1976D2", alpha=0.7)
    ax.barh(i, right - base_be, left=base_be, height=0.6, color="#E53935", alpha=0.7)
    if left < base_be:
        ax.text(left - off, i, fmt(lo_lab), ha="right", va="center", fontsize=7,
                color="#1976D2")
    if right > base_be:
        ax.text(right + off, i, fmt(hi_lab), ha="left", va="center", fontsize=7,
                color="#E53935")
ax.axvline(base_be, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
ax.set_yticks(range(len(tdf)))
ax.set_yticklabels(tdf["parameter"], fontsize=8)
ax.set_xlabel("Break-even: unplanned ICU transfers averted per 1,000 patient-days",
              fontsize=10)
ax.set_xlim(lo_all.min() - span * 0.12, hi_all.max() + span * 0.12)
ax.legend(handles=[Patch(facecolor="#1976D2", alpha=0.7, label="Lower threshold"),
                   Patch(facecolor="#E53935", alpha=0.7, label="Higher threshold")],
          fontsize=8, loc="lower right")
ax.text(0.02, -0.11,
        f"Dashed line: base case ({base_be:.2f} per 1,000 patient-days). "
        "Numbers at bar ends show the parameter values tested.",
        transform=ax.transAxes, fontsize=7, color="gray")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.subplots_adjust(left=0.36, right=0.96, top=0.95, bottom=0.15)
fig.savefig(FIGURES / "fig5_tornado.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig5_tornado.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Figure 5 saved to {FIGURES}")


# ══════════════════════════════════════════════════════════════════════
# Released-time and alarm-burden scenarios (all devices, primary B)
# ══════════════════════════════════════════════════════════════════════
SCENARIOS = {
    "Base case (20 s released)": {},
    "No nurse time released (0 s)": {"released_sec": 0},
    "Full counting time released (80 s)": {"released_sec": FULL_COUNT_SEC},
    "Alarm handling +5 min/patient-day": {"alarm_extra_min": 5},
}
sc_rows = []
for name in DEVICES:
    for sc, change in SCENARIOS.items():
        p = BASE.copy()
        p.update(change)
        inc = incremental(name, p)
        for ev_name in ("Japan, fee schedule", "UK, NHS cost collection"):
            be = breakeven_per_1000(inc, EV[ev_name]["value"])
            sc_rows.append({
                "device_scenario": name, "scenario": sc,
                "event_value_scenario": ev_name,
                "incremental_cost_jpd": round(inc, 1),
                "breakeven_per_1000pd": round(be, 2),
                "q_required_pct_at_ref_rate": round(q_required(be) * 100, 1),
            })
    # Additional alarm-handling time at which q_required reaches 100% at I_REF
    for ev_name in ("Japan, fee schedule", "UK, NHS cost collection"):
        b = EV[ev_name]["value"]
        extra = (I_REF * b / 1000 - incremental(name)) * 60 / BASE["nurse_hourly"]
        sc_rows.append({
            "device_scenario": name,
            "scenario": "Alarm handling time (min/pd) at which q_required = 100%",
            "event_value_scenario": ev_name,
            "incremental_cost_jpd": np.nan,
            "breakeven_per_1000pd": I_REF,
            "q_required_pct_at_ref_rate": 100.0,
            "threshold_extra_alarm_min_per_pd": round(extra, 1),
        })
sc_df = pd.DataFrame(sc_rows)
sc_df.to_csv(TABLES / "table6_scenario_analysis.csv", index=False)
print(f"Table 6 saved: {TABLES / 'table6_scenario_analysis.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Two-way threshold analysis: released time x device staff time
# ══════════════════════════════════════════════════════════════════════
tw_rows = []
for sec in (0, 20, 40, 60, 80):
    for minutes in (1, 3, 5, 8):
        p = BASE.copy()
        p["released_sec"] = sec
        inc = incremental(REP, p, staff_min=minutes)
        row = {"released_sec": sec, "device_staff_min_per_pd": minutes,
               "incremental_cost_jpd": round(inc, 1)}
        for tag, b in (("japan_fee_schedule", B_JP), ("uk_cost_collection", B_UK)):
            be = breakeven_per_1000(inc, b)
            row[f"breakeven_per_1000pd_{tag}"] = round(be, 2)
            row[f"q_required_pct_{tag}"] = round(q_required(be) * 100, 1)
        tw_rows.append(row)
pd.DataFrame(tw_rows).to_csv(TABLES / "table7_two_way.csv", index=False)
print(f"Table 7 saved: {TABLES / 'table7_two_way.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Stress test: all one-way ranges at their extremes simultaneously.
# Reported for transparency only; this joint state is not plausible and is
# not used as evidence of robustness.
# ══════════════════════════════════════════════════════════════════════
def corner(favour):
    p = BASE.copy()
    hi = favour  # True = values favouring the device
    p.update({
        # The nurse wage enters both device staff time (a cost) and released time
        # (a saving). With 80 s released and 1 min staff time a higher wage
        # favours the device; with 0 s released and 8 min it disfavours it, so
        # ¥4,200 is the extreme value in both corners.
        "nurse_hourly": 4200,
        "released_sec": FULL_COUNT_SEC if hi else 0,
        "obs_frequency": 8 if hi else 2,
        "occupancy": 0.95 if hi else 0.75,
        # Price endpoints are expressed at the base exchange rate; the ±15%
        # exchange-rate extreme is applied on top (effective ¥340,000 and
        # ¥1,150,000 per bed), as stated in Supplementary S2.
        "price_scale": (400_000 if hi else 1_000_000) / REP_PRICE,
        "life_monitor": 10 if hi else 5,
        "maint_rate": 0.05 if hi else 0.12,
        "fx_gbp": BASE["fx_gbp"] * (0.85 if hi else 1.15),
    })
    b = B_JP_CLAIMS if hi else B_JP
    inc = incremental(REP, p, staff_min=1 if hi else 8)
    return inc, b


st_rows = []
for label, fav in (("All values favouring the device", True),
                   ("All values disfavouring the device", False)):
    inc, b = corner(fav)
    be = breakeven_per_1000(inc, b)
    # ΔC <= 0: no events need to be averted; a threshold is not defined
    st_rows.append({"stress_test": label, "incremental_cost_jpd": round(inc, 1),
                    "event_value_jpy": round(b),
                    "breakeven_per_1000pd": round(be, 2) if inc > 0 else np.nan,
                    "q_required_pct_at_ref_rate":
                        round(q_required(be) * 100, 1) if inc > 0 else np.nan,
                    "note": "" if inc > 0 else "Incremental cost <= 0; no threshold"})
pd.DataFrame(st_rows).to_csv(TABLES / "table8_stress_test.csv", index=False)
print(f"Table 8 saved: {TABLES / 'table8_stress_test.csv'}")


# ══════════════════════════════════════════════════════════════════════
# Figure 6: Required avoidable fraction versus baseline event rate
# ══════════════════════════════════════════════════════════════════════
rates = np.linspace(1, 12, 221)
dev_colors = ["#2E7D32", "#1565C0", "#F9A825", "#6A1B9A", "#C62828"]
fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
for ax, ev_name in zip(axes, ("Japan, fee schedule", "UK, NHS cost collection")):
    b = EV[ev_name]["value"]
    for color, name in zip(dev_colors, DEVICES):
        be = breakeven_per_1000(incremental(name), b)
        ax.plot(rates, q_required(be, rates) * 100, color=color, linewidth=1.8,
                label=DEVICES[name]["short"])
    ax.axhline(100, color="black", linewidth=1)
    ax.axvline(I_REF, color="gray", linestyle=":", linewidth=1)
    ax.text(I_REF + 0.15, 185, f"I = {I_REF:g}/1,000 patient-days\n(illustrative reading point)",
            fontsize=7, color="gray", va="top")
    ax.text(11.9, 103, "q_required > 100%: not attainable", fontsize=7,
            ha="right", va="bottom")
    ax.set_xlim(1, 12)
    ax.set_ylim(0, 200)
    ax.set_xlabel("Baseline unplanned ICU transfer rate, I\n"
                  "(per 1,000 patient-days)", fontsize=9)
    ax.set_title(f"{'a' if ax is axes[0] else 'b'}  {ev_name} "
                 f"(V = ¥{b:,.0f})", fontsize=9, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
axes[0].set_ylabel("Required avoidable fraction, q_required (%)", fontsize=9)
axes[0].legend(fontsize=8, loc="upper right")
plt.tight_layout()
fig.savefig(FIGURES / "fig6_required_fraction.pdf", dpi=300, bbox_inches="tight")
fig.savefig(FIGURES / "fig6_required_fraction.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"Figure 6 saved to {FIGURES}")

if __name__ == "__main__":
    print("\n=== 04_sensitivity.py complete ===")
