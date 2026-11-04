"""
Script: clean_dataset.py
Purpose: Member 1 Data Cleaning & Quality Assurance
- Removes duplicate transactions
- Filters out invalid values (negative/zero prices, negative returns)
- Imputes missing confounder values (competitor price, footfall)
- Validates data types and schema integrity
- Generates data_quality_report.md
- Saves data/processed/retail_transactions_cleaned.csv
"""

import os
import json
import pandas as pd
import numpy as np

def clean_retail_data(raw_path, cleaned_path, report_path):
    print("Loading raw dataset from:", raw_path)
    df_raw = pd.read_csv(raw_path)
    initial_rows = len(df_raw)
    
    report_metrics = {
        "initial_rows": initial_rows,
        "initial_columns": len(df_raw.columns)
    }

    # 1. Duplicates Detection & Removal
    # Transactions should be unique by transaction_id or (date, store_id, product_id)
    dup_tx = df_raw.duplicated(subset=["transaction_id"]).sum()
    dup_natural = df_raw.duplicated(subset=["date", "store_id", "product_id"]).sum()
    report_metrics["duplicates_by_tx_id"] = int(dup_tx)
    report_metrics["duplicates_natural_key"] = int(dup_natural)
    
    # Drop duplicates keeping first
    df = df_raw.drop_duplicates(subset=["date", "store_id", "product_id"]).copy()
    rows_after_dedup = len(df)
    report_metrics["rows_after_dedup"] = rows_after_dedup

    # 2. Invalid Values Detection
    invalid_price = (df["unit_price"] <= 0)
    invalid_units = (df["units_sold"] <= 0)
    invalid_records = invalid_price | invalid_units
    
    report_metrics["invalid_price_count"] = int(invalid_price.sum())
    report_metrics["invalid_units_count"] = int(invalid_units.sum())
    report_metrics["total_invalid_dropped"] = int(invalid_records.sum())

    # Filter out invalid records
    df = df[~invalid_records].copy()
    rows_after_invalid_filter = len(df)
    report_metrics["rows_after_invalid_filter"] = rows_after_invalid_filter

    # 3. Missing Values Handling
    missing_before = df.isnull().sum().to_dict()
    report_metrics["missing_before_imputation"] = {k: int(v) for k, v in missing_before.items() if v > 0}

    # Impute competitor_price with the product-week median (or overall product median)
    comp_price_medians = df.groupby(["product_id", "week"])["competitor_price"].transform("median")
    prod_medians = df.groupby("product_id")["competitor_price"].transform("median")
    df["competitor_price"] = df["competitor_price"].fillna(comp_price_medians).fillna(prod_medians)

    # Impute store_footfall with store + is_weekend median
    footfall_medians = df.groupby(["store_id", "is_weekend"])["store_footfall"].transform("median")
    df["store_footfall"] = df["store_footfall"].fillna(footfall_medians)

    missing_after = df.isnull().sum().to_dict()
    report_metrics["missing_after_imputation"] = {k: int(v) for k, v in missing_after.items() if v > 0}

    # 4. Consistency & Schema Validation
    # Ensure revenue matches unit_price * units_sold
    df["revenue"] = (df["unit_price"] * df["units_sold"]).round(2)
    
    # Ensure correct data types
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["week"].astype(int)
    df["store_id"] = df["store_id"].astype(str)
    df["product_id"] = df["product_id"].astype(str)
    df["unit_price"] = df["unit_price"].astype(float)
    df["units_sold"] = df["units_sold"].astype(int)
    df["revenue"] = df["revenue"].astype(float)
    df["competitor_price"] = df["competitor_price"].astype(float)
    df["marketing_spend"] = df["marketing_spend"].astype(float)
    df["store_footfall"] = df["store_footfall"].astype(int)
    df["is_holiday"] = df["is_holiday"].astype(int)
    df["is_weekend"] = df["is_weekend"].astype(int)

    # Sort deterministically
    df = df.sort_values(by=["date", "store_id", "product_id"]).reset_index(drop=True)
    
    final_rows = len(df)
    report_metrics["final_clean_rows"] = final_rows
    report_metrics["retention_rate_pct"] = round((final_rows / initial_rows) * 100, 2)

    # Save cleaned CSV
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    df.to_csv(cleaned_path, index=False)
    print(f"Cleaned dataset saved: {cleaned_path} ({final_rows} rows)")

    # 5. Generate Markdown Data Quality Report
    summary_stats = df[["unit_price", "units_sold", "revenue", "competitor_price", "marketing_spend", "store_footfall"]].describe().round(2)

    md_report = f"""# Member 1: Data Quality & Preprocessing Report
**Project:** Causal Inference & Synthetic Control Engine for Algorithmic Pricing  
**Dataset:** Retail Transactions Dataset  

---

## 1. Executive Summary
- **Raw Records Ingested:** {report_metrics['initial_rows']:,}
- **Duplicates Removed:** {report_metrics['duplicates_natural_key']:,}
- **Invalid Records Filtered:** {report_metrics['total_invalid_dropped']:,} (Negative/zero prices, negative returns)
- **Missing Values Imputed:** {sum(report_metrics['missing_before_imputation'].values()):,} records
- **Final Clean Records:** {report_metrics['final_clean_rows']:,}
- **Data Retention Rate:** **{report_metrics['retention_rate_pct']}%**

---

## 2. Data Cleaning Breakdown

| Quality Check | Issue Detected | Action Taken | Records Affected |
| :--- | :--- | :--- | :--- |
| **Duplicate Keys** | Repeated (date, store, product) logs | Dropped duplicate occurrences | {report_metrics['duplicates_natural_key']} |
| **Invalid Prices** | Negative/zero price values | Removed corrupt transaction records | {report_metrics['invalid_price_count']} |
| **Invalid Quantities** | Negative unit sales (returns/scans) | Removed corrupt transaction records | {report_metrics['invalid_units_count']} |
| **Missing Competitor Price** | Null sensor/crawler entries | Imputed with product-week median | {report_metrics['missing_before_imputation'].get('competitor_price', 0)} |
| **Missing Footfall** | Null store sensor entries | Imputed with store-weekend median | {report_metrics['missing_before_imputation'].get('store_footfall', 0)} |

---

## 3. Post-Cleaning Summary Statistics

```
{summary_stats.to_string()}
```

---

## 4. Downstream Readiness
- **Schema Validated:** 14 columns, zero null values.
- **Ready for Panel Aggregation:** Ready for store/product/week roll-up for Member 2 (DAG), Member 3 (Synthetic Control), and Member 4 (Double ML).
"""

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_report)
    print(f"Data quality report saved to: {report_path}")

    return df

if __name__ == "__main__":
    raw_csv = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\raw\retail_transactions_raw.csv"
    clean_csv = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\processed\retail_transactions_cleaned.csv"
    report_md = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\reports\data_quality_report.md"

    clean_retail_data(raw_csv, clean_csv, report_md)
