#!/usr/bin/env python3
"""
model_core.py
-------------
Single source of truth for the cost and break-even calculations.
Imported by 03_cost_model.py and 04_sensitivity.py so that the main-text
tables and the sensitivity analyses use the same cost function and inputs.

Definitions (per patient-day unless stated):
  gross device cost  = capital + maintenance + sensor replacement
                       + consumables + device-related staff time
  released time      = nurse time released from manual RR counting
                       (observations/day x released seconds/observation)
  incremental cost   = gross device cost - released time            (ΔC)
  break-even         = ΔC / V x 1,000   (events per 1,000 patient-days)
  q_required         = break-even / I   (I = baseline event rate per
                                         1,000 patient-days)
where V is the event value: the incremental cost assumed to be averted
when one unplanned ICU transfer is averted.
"""

import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

params = pd.read_csv(DATA / "cost_parameters.csv")


def get_param(pid):
    """Get parameter value by parameter_id."""
    row = params[params["parameter_id"] == pid]
    if row.empty:
        raise ValueError(f"Parameter {pid} not found")
    return float(row["value"].iloc[0])


# ── Base case (Japan) ────────────────────────────────────────────────
BASE = {
    "nurse_hourly": get_param("COST_JP03"),      # JPY/hour
    "obs_frequency": get_param("MODEL02"),       # observations/patient-day
    "released_sec": get_param("MODEL08"),        # s released per observation
    "occupancy": get_param("MODEL04"),
    "ward_beds": get_param("MODEL03"),
    "life_monitor": get_param("MODEL05"),        # years
    "maint_rate": get_param("MODEL07"),          # proportion of price/year
    "alarm_extra_min": 0.0,                      # added alarm handling, min/pd
    "price_scale": 1.0,                          # multiplier on device price
    "fx_usd": get_param("FX01"),
    "fx_gbp": get_param("FX02"),
    "fx_aud": get_param("FX04"),
}

FULL_COUNT_SEC = get_param("MODEL01")            # 60 s count + 20 s documentation
I_REF = get_param("RATE01")                      # illustrative reading point, per 1,000 pd


# ── Device scenarios ─────────────────────────────────────────────────
# price_* : purchase price per bed in source currency (0 = no capital)
# sensor_gbp_year : annual sensor replacement per bed (NICE MIB49)
# maint : general maintenance at maint_rate x price applies (capital devices)
# staff_min : device-related staff time incl. alarm handling (min/pd)
DEVICES = {
    "Radar sensor (Guardian M10-type)": {
        "short": "Radar", "category": "Non-contact",
        "price_jpy": 500_000, "maint": True, "consumable": None,
        "staff_min": 2},
    "Under-mattress sensor (EarlySense-type)": {
        "short": "Under-mattress", "category": "Non-contact",
        "price_gbp": 35_000 / 10, "sensor_gbp_year": 475, "maint": True,
        "consumable": None, "staff_min": 3},
    "Wearable patch (RespiraSense-type)": {
        "short": "Wearable patch", "category": "Wearable",
        # Patch cost only; the kit (GBP 5,000 per kit with six reusable lobes; one
        # kit per ward according to the company) and installation and network costs
        # (GBP 12,000/hospital) reported in NICE MIB299 are not included
        # (illustrative sizes in Supplementary S1).
        "maint": False, "consumable": ("gbp", 35 / 7), "staff_min": 5},
    "Bedside monitor (impedance RR)": {
        "short": "Bedside monitor", "category": "Impedance",
        "price_jpy": 1_350_000, "maint": True, "consumable": ("jpy", 200),
        "staff_min": 4},
    "Capnography (Capnostream-type)": {
        "short": "Capnography", "category": "Capnography",
        "price_usd": 4_500, "maint": True, "consumable": ("usd", 10),
        "staff_min": 5},
}
REPRESENTATIVE = "Under-mattress sensor (EarlySense-type)"


def device_price_jpy(dev, p):
    if "price_jpy" in dev:
        price = dev["price_jpy"]
    elif "price_gbp" in dev:
        price = dev["price_gbp"] * p["fx_gbp"]
    elif "price_usd" in dev:
        price = dev["price_usd"] * p["fx_usd"]
    else:
        price = 0.0
    return price * p["price_scale"]


def released_pd(p):
    """Value of nurse time released from manual RR counting (JPY/pd)."""
    return p["nurse_hourly"] * p["released_sec"] / 3600 * p["obs_frequency"]


def device_components(name, p=None, staff_min=None):
    """Per-patient-day cost components of one device scenario (JPY)."""
    p = BASE if p is None else p
    dev = DEVICES[name]
    pd_per_bed = p["occupancy"] * 365
    price = device_price_jpy(dev, p)
    capital = price / p["life_monitor"] / pd_per_bed if price else 0.0
    maint = price * p["maint_rate"] / pd_per_bed if dev["maint"] else 0.0
    sensor = dev.get("sensor_gbp_year", 0) * p["fx_gbp"] / pd_per_bed
    cons = 0.0
    if dev["consumable"]:
        cur, amount = dev["consumable"]
        cons = amount * {"jpy": 1, "usd": p["fx_usd"], "gbp": p["fx_gbp"]}[cur]
    minutes = (dev["staff_min"] if staff_min is None else staff_min) \
        + p["alarm_extra_min"]
    staff = minutes / 60 * p["nurse_hourly"]
    gross = capital + maint + sensor + cons + staff
    rel = released_pd(p)
    return {
        "capital_jpd": capital, "maintenance_jpd": maint,
        "sensor_replacement_jpd": sensor, "consumables_jpd": cons,
        "device_staff_jpd": staff, "device_staff_min": minutes,
        "gross_device_cost_jpd": gross, "released_manual_time_jpd": rel,
        "incremental_jpd": gross - rel,
    }


def incremental(name, p=None, staff_min=None):
    return device_components(name, p, staff_min)["incremental_jpd"]


# ── Event value V ────────────────────────────────────────────────────
# Assumption: one averted unplanned ICU transfer averts 3 ICU days and
# 5 subsequent ward days (MODEL09, MODEL10).
ICU_DAYS = get_param("MODEL09")
WARD_DAYS = get_param("MODEL10")


def event_values(p=None):
    """Event-value scenarios (JPY per event).

    role: primary / variant (endpoint = unplanned ICU transfer; q_required
    is reported) or separate (different endpoint or construct; break-even
    shown for reference only and not pooled with the others).
    """
    p = BASE if p is None else p
    jp_ward = get_param("COST_JP01")
    return {
        "Japan, fee schedule": {
            "value": ICU_DAYS * get_param("COST_JP02") + WARD_DAYS * jp_ward,
            "role": "primary", "endpoint": "Unplanned ICU transfer",
            "construct": "Payment (national fee schedule)"},
        "UK, NHS cost collection": {
            "value": (ICU_DAYS * get_param("COST_UK01")
                      + WARD_DAYS * get_param("COST_UK02")) * p["fx_gbp"],
            "role": "primary", "endpoint": "Unplanned ICU transfer",
            "construct": "Provider cost (2020/21 cost collection)"},
        "Japan, claims-based ICU charges": {
            "value": ICU_DAYS * get_param("COST_JP05") + WARD_DAYS * jp_ward,
            "role": "variant", "endpoint": "Unplanned ICU transfer",
            "construct": "Payment (claims-based charges, ICU days)"},
        "Australia, deterioration episode": {
            "value": get_param("COST_AU01") * p["fx_aud"],
            "role": "separate",
            "endpoint": "MET call, cardiac arrest or unplanned ICU "
                        "admission within 72 h of admission",
            "construct": "Regression-adjusted treatment cost"},
        "USA, operating margin": {
            "value": get_param("COST_US04") * p["fx_usd"],
            "role": "separate",
            "endpoint": "Transfer to a higher level of care (intermediate "
                        "or critical care)",
            "construct": "Hospital operating-margin effect"},
    }


def breakeven_per_1000(inc, b):
    return inc / b * 1000


def q_required(be_per_1000, rate=None):
    """Required avoidable fraction (proportion); may exceed 1."""
    return be_per_1000 / (I_REF if rate is None else rate)


def patient_days_year(p=None):
    p = BASE if p is None else p
    return p["ward_beds"] * p["occupancy"] * 365
