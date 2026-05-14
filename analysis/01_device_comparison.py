#!/usr/bin/env python3
"""
01_device_comparison.py
-----------------------
Load device_characteristics.csv and accuracy_studies.csv,
produce Table 1 (device comparison) and Table 2 (accuracy summary)
for the manuscript.

Outputs:
  ../tables/table1_device_comparison.csv
  ../tables/table2_accuracy_summary.csv
"""

import os, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TABLES = ROOT / "tables"
TABLES.mkdir(exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────
devices = pd.read_csv(DATA / "device_characteristics.csv")
accuracy = pd.read_csv(DATA / "accuracy_studies.csv")

# ── Table 1: Device Comparison ───────────────────────────────────────
table1_cols = [
    "device_id", "device_name", "manufacturer", "measurement_principle",
    "category", "contact_type", "fda_cleared", "ce_marked",
    "emr_integration", "abnormal_pattern_detection",
    "price_estimate_local", "price_currency", "current_status"
]
table1 = devices[table1_cols].copy()
table1.to_csv(TABLES / "table1_device_comparison.csv", index=False)
print(f"Table 1 saved: {TABLES / 'table1_device_comparison.csv'}")
print(f"  {len(table1)} devices")

# ── Table 2: Accuracy Summary ────────────────────────────────────────
table2_cols = [
    "study_id", "device_id", "first_author", "year", "journal",
    "n_patients", "reference_standard",
    "bias_bpm", "loa_lower_bpm", "loa_upper_bpm",
    "sensitivity", "specificity", "threshold_within_pct",
    "population", "notes"
]
# Merge device name
table2 = accuracy[table2_cols].merge(
    devices[["device_id", "device_name"]], on="device_id", how="left"
)
# Reorder
front = ["study_id", "device_name"]
table2 = table2[front + [c for c in table2.columns if c not in front]]
table2.to_csv(TABLES / "table2_accuracy_summary.csv", index=False)
print(f"Table 2 saved: {TABLES / 'table2_accuracy_summary.csv'}")
print(f"  {len(table2)} accuracy records")

if __name__ == "__main__":
    print("\n=== 01_device_comparison.py complete ===")
