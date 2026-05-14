#!/usr/bin/env python3
"""
05_generate_all.py
------------------
Master script: run all analysis scripts in order.

Usage:
  cd analysis/
  python 05_generate_all.py
"""

import subprocess
import sys
import pathlib

SCRIPTS = [
    "01_device_comparison.py",
    "02_accuracy_analysis.py",
    "03_cost_model.py",
    "04_sensitivity.py",
    "06_study_overview.py",
]

def main():
    script_dir = pathlib.Path(__file__).resolve().parent
    all_ok = True

    for script in SCRIPTS:
        path = script_dir / script
        print(f"\n{'='*60}")
        print(f"Running: {script}")
        print(f"{'='*60}")
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(script_dir),
            capture_output=False
        )
        if result.returncode != 0:
            print(f"ERROR: {script} failed with return code {result.returncode}")
            all_ok = False

    print(f"\n{'='*60}")
    if all_ok:
        print("All scripts completed successfully.")
        print("\nGenerated outputs:")
        for d in ["tables", "figures"]:
            output_dir = script_dir.parent / d
            if output_dir.exists():
                for f in sorted(output_dir.iterdir()):
                    print(f"  {d}/{f.name}")
    else:
        print("Some scripts failed. Check output above.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
