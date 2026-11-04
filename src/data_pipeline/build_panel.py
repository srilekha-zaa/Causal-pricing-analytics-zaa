"""
Script: build_panel.py
Purpose: Member 1 Panel Preparation
- Transforms daily cleaned transactions into Store x Product x Week panel data
- Derives causal indicators (is_treated_store, is_post_treatment, treatment_active)
- Computes log transformations for econometric / causal modeling (DML & SCM)
- Exports data/processed/store_product_week_panel.csv
"""

import os
import pandas as pd
import numpy as np

def build_store_week_panel(clean_tx_path, panel_output_path):
    print("Loading cleaned transactions from:", clean_tx_path)
    df = pd.read_csv(clean_tx_path)
    df["date"] = pd.to_datetime(df["date"])

    # Aggregate by store_id, product_id, product_name, week
    panel = df.groupby(["store_id", "product_id", "product_name", "week"]).agg(
        avg_unit_price=("unit_price", "mean"),
        weighted_unit_price=("revenue", lambda s: s.sum() / df.loc[s.index, "units_sold"].sum()),
        total_units_sold=("units_sold", "sum"),
        total_revenue=("revenue", "sum"),
        avg_competitor_price=("competitor_price", "mean"),
        total_marketing_spend=("marketing_spend", "sum"),
        avg_store_footfall=("store_footfall", "mean"),
        holiday_days=("is_holiday", "sum"),
        days_recorded=("date", "count")
    ).reset_index()

    # Round numeric values
    panel["avg_unit_price"] = panel["avg_unit_price"].round(2)
    panel["weighted_unit_price"] = panel["weighted_unit_price"].round(2)
    panel["total_revenue"] = panel["total_revenue"].round(2)
    panel["avg_competitor_price"] = panel["avg_competitor_price"].round(2)
    panel["total_marketing_spend"] = panel["total_marketing_spend"].round(2)
    panel["avg_store_footfall"] = panel["avg_store_footfall"].round(1)

    # Causal Identification Columns
    # Store_1 is the treated store where dynamic pricing experiment launched at Week 36
    panel["is_treated_store"] = (panel["store_id"] == "Store_1").astype(int)
    panel["is_post_treatment"] = (panel["week"] >= 36).astype(int)
    panel["treatment_active"] = (
        (panel["is_treated_store"] == 1) & 
        (panel["is_post_treatment"] == 1) & 
        (panel["product_id"] == "PROD_101")
    ).astype(int)

    # Elasticity / Double ML log variables
    panel["log_price"] = np.log(panel["avg_unit_price"]).round(4)
    panel["log_units"] = np.log(panel["total_units_sold"]).round(4)
    panel["log_revenue"] = np.log(panel["total_revenue"]).round(4)
    panel["log_competitor_price"] = np.log(panel["avg_competitor_price"]).round(4)

    # Sort deterministically
    panel = panel.sort_values(by=["product_id", "store_id", "week"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(panel_output_path), exist_ok=True)
    panel.to_csv(panel_output_path, index=False)
    print(f"Panel dataset successfully created: {panel_output_path}")
    print(f"Dimensions: {panel.shape[0]} store-product-week rows, {panel.shape[1]} columns")
    print(f"Stores: {panel['store_id'].nunique()} | Weeks: {panel['week'].nunique()} | Products: {panel['product_id'].nunique()}")

    return panel

if __name__ == "__main__":
    clean_csv = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\processed\retail_transactions_cleaned.csv"
    panel_csv = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\processed\store_product_week_panel.csv"

    build_store_week_panel(clean_csv, panel_csv)
