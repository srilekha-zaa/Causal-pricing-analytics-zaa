"""
Master Runner: run_member1_pipeline.py
Purpose: Runs the entire Member 1 Data Engineering workflow in sequence:
1. Generates realistic raw retail transactions with real-world noise.
2. Cleans duplicates, filters invalid values, and imputes missing confounders.
3. Aggregates data into Store x Product x Week panel format.
4. Generates EDA visualization figures and data quality reports.
"""

import os
import subprocess
import sys
import time

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, "src", "data_pipeline")

    steps = [
        ("Step 1: Raw Data Generation", os.path.join(src_dir, "generate_dataset.py")),
        ("Step 2: Data Cleaning & QA", os.path.join(src_dir, "clean_dataset.py")),
        ("Step 3: Panel Dataset Construction", os.path.join(src_dir, "build_panel.py")),
        ("Step 4: Exploratory Data Analysis & Plots", os.path.join(src_dir, "eda_analysis.py"))
    ]

    print("=" * 70)
    print("[START] MEMBER 1: DATA ENGINEERING & PIPELINE EXECUTION")
    print("=" * 70)

    start_total = time.time()
    for name, script_path in steps:
        print(f"\n>> Running {name}...")
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR] in {name}:")
            print(res.stderr)
            sys.exit(1)
        else:
            print(res.stdout.strip())
            print(f"[OK] {name} finished successfully.")

    print("\n" + "=" * 70)
    print(f"[SUCCESS] MEMBER 1 PIPELINE COMPLETE in {round(time.time() - start_total, 2)}s!")
    print("Deliverables ready:")
    print("  * Raw CSV:   data/raw/retail_transactions_raw.csv")
    print("  * Clean CSV: data/processed/retail_transactions_cleaned.csv")
    print("  * Panel CSV: data/processed/store_product_week_panel.csv")
    print("  * QA Report: reports/data_quality_report.md")
    print("  * EDA Plots: reports/eda_figures/ (4 publication figures)")
    print("=" * 70)

if __name__ == "__main__":
    main()
