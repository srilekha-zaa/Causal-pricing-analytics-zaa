"""
Script: eda_analysis.py
Purpose: Member 1 Exploratory Data Analysis & Visualizations
Generates publication-ready charts for the team:
1. 01_price_trajectories_intervention.png
2. 02_weekly_sales_volume_and_treatment.png
3. 03_parallel_trends_validation.png
4. 04_confounders_correlation_matrix.png
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

def run_eda(panel_path, output_dir):
    print("Loading panel dataset from:", panel_path)
    df = pd.read_csv(panel_path)
    os.makedirs(output_dir, exist_ok=True)

    # Focus on target product PROD_101 for treatment analysis
    df_prod1 = df[df["product_id"] == "PROD_101"].copy()

    # -------------------------------------------------------------
    # 1. Price Trajectories: Store 1 vs Donor Stores
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 5))
    donor_stores = [f"Store_{i}" for i in range(2, 11)]
    for store in donor_stores:
        sub = df_prod1[df_prod1["store_id"] == store]
        plt.plot(sub["week"], sub["avg_unit_price"], color="#b0bec5", alpha=0.5, linewidth=1.2, linestyle="--")
    
    # Plot Treated Store
    sub_treated = df_prod1[df_prod1["store_id"] == "Store_1"]
    plt.plot(sub_treated["week"], sub_treated["avg_unit_price"], color="#d32f2f", linewidth=2.8, label="Treated Unit (Store_1)")
    plt.plot([], [], color="#78909c", linestyle="--", label="Donor Pool Stores (Store 2-10)")
    
    plt.axvline(x=35.5, color="#263238", linestyle=":", linewidth=2, label="Week 36: Algorithmic Price Hike (+15%)")
    plt.title("Product 101: Price Trajectories Before & After Intervention", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Week of Year (1 - 52)", fontsize=12)
    plt.ylabel("Average Unit Price ($)", fontsize=12)
    plt.legend(frameon=True, facecolor="white", loc="upper left")
    
    p1 = os.path.join(output_dir, "01_price_trajectories_intervention.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"Saved: {p1}")

    # -------------------------------------------------------------
    # 2. Sales Volume Trends: Store 1 vs Donor Average
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 5))
    donor_avg_sales = df_prod1[df_prod1["store_id"].isin(donor_stores)].groupby("week")["total_units_sold"].mean()
    treated_sales = sub_treated.set_index("week")["total_units_sold"]

    plt.plot(donor_avg_sales.index, donor_avg_sales.values, color="#1976d2", linewidth=2.2, linestyle="-.", label="Donor Pool Mean Sales")
    plt.plot(treated_sales.index, treated_sales.values, color="#d32f2f", linewidth=2.5, label="Store_1 (Treated Store) Actual Sales")
    
    plt.axvline(x=35.5, color="#263238", linestyle=":", linewidth=2, label="Week 36: Intervention Start")
    plt.fill_between(range(36, 53), 0, max(treated_sales.max(), donor_avg_sales.max()) * 1.15, color="#ffebee", alpha=0.4, label="Post-Treatment Evaluation Window")
    
    plt.title("Weekly Units Sold: Treated Store vs. Donor Pool Average", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Week of Year (1 - 52)", fontsize=12)
    plt.ylabel("Weekly Units Sold", fontsize=12)
    plt.ylim(0, max(treated_sales.max(), donor_avg_sales.max()) * 1.15)
    plt.legend(frameon=True, facecolor="white", loc="lower left")

    p2 = os.path.join(output_dir, "02_weekly_sales_volume_and_treatment.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"Saved: {p2}")

    # -------------------------------------------------------------
    # 3. Pre-Treatment Parallel Trends Check (Normalized Index)
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    pre_treated = treated_sales.loc[1:35]
    pre_donor = donor_avg_sales.loc[1:35]
    
    # Normalize index: Week 1 = 100
    norm_treated = (pre_treated / pre_treated.iloc[0]) * 100
    norm_donor = (pre_donor / pre_donor.iloc[0]) * 100

    plt.plot(norm_treated.index, norm_treated.values, color="#d32f2f", linewidth=2.4, marker="o", markersize=4, label="Store_1 (Pre-treatment Index)")
    plt.plot(norm_donor.index, norm_donor.values, color="#1976d2", linewidth=2.4, marker="s", markersize=4, linestyle="--", label="Donor Pool Average Index")
    
    plt.title("Pre-Treatment Parallel Trends Check (Weeks 1 to 35, Baseline = 100)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Pre-treatment Week", fontsize=12)
    plt.ylabel("Sales Volume Index (Week 1 = 100)", fontsize=12)
    plt.legend(frameon=True, facecolor="white", loc="upper left")

    p3 = os.path.join(output_dir, "03_parallel_trends_validation.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"Saved: {p3}")

    # -------------------------------------------------------------
    # 4. Confounder Correlation Heatmap
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    corr_vars = [
        "avg_unit_price", "total_units_sold", "total_revenue",
        "avg_competitor_price", "total_marketing_spend", "avg_store_footfall", "holiday_days"
    ]
    corr_labels = [
        "Price", "Units Sold", "Revenue",
        "Competitor Price", "Marketing Spend", "Footfall", "Holidays"
    ]
    corr_mat = df_prod1[corr_vars].corr()
    corr_mat.columns = corr_labels
    corr_mat.index = corr_labels

    sns.heatmap(corr_mat, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, cbar=True, square=True)
    plt.title("Confounder & Target Correlation Matrix (Product 101)", fontsize=13, fontweight="bold", pad=12)

    p4 = os.path.join(output_dir, "04_confounders_correlation_matrix.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"Saved: {p4}")

    print("All EDA charts generated successfully.")

def get_project_root():
    curr = os.path.dirname(os.path.abspath(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "data")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if __name__ == "__main__":
    root = get_project_root()
    panel_csv = os.path.join(root, "data", "processed", "store_product_week_panel.csv")
    charts_dir = os.path.join(root, "reports", "eda_figures")

    run_eda(panel_csv, charts_dir)
