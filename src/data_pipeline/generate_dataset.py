"""
Script: generate_dataset.py
Purpose: Generates a realistic retail transaction dataset with:
- 10 stores (Store_1: treated, Store_2 to Store_10: donor pool)
- 52 weeks of daily transactions for 3 products
- Confounders: seasonal cycle, marketing spend, competitor pricing, footfall, holiday flag
- Algorithmic pricing treatment on Store_1 starting at Week 36 (+15% price shift)
- Injected real-world data flaws: missing values, duplicates, and invalid records for Member 1 to clean.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_retail_data(seed=42):
    np.random.seed(seed)
    
    start_date = datetime(2025, 1, 1)
    n_days = 364  # exactly 52 weeks
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    
    stores = [f"Store_{i}" for i in range(1, 11)]
    products = [
        {"id": "PROD_101", "name": "Flagship Energy Drink 500ml", "base_price": 3.50, "elasticity": -1.5},
        {"id": "PROD_102", "name": "Classic Cola 1.5L", "base_price": 2.20, "elasticity": -1.2},
        {"id": "PROD_103", "name": "Sparkling Mineral Water 1L", "base_price": 1.80, "elasticity": -0.9}
    ]
    
    # Store base multipliers (size / baseline demand)
    store_multiplier = {
        f"Store_{i}": 1.0 + 0.05 * (i % 3) - 0.03 * (i % 2) for i in range(1, 11)
    }
    # Treated store (Store_1) has close donor peers (Store_2, Store_3, Store_4, etc.)
    store_multiplier["Store_1"] = 1.15
    store_multiplier["Store_2"] = 1.12
    store_multiplier["Store_3"] = 1.18
    store_multiplier["Store_4"] = 1.05
    store_multiplier["Store_5"] = 1.10

    records = []
    tx_counter = 1000000

    print("Generating daily transactions across 10 stores and 52 weeks...")

    for d_idx, cur_date in enumerate(dates):
        week_num = (d_idx // 7) + 1
        day_of_week = cur_date.weekday()
        is_weekend = 1 if day_of_week in [5, 6] else 0
        
        # Macro seasonality (sine wave peaking in summer around week 26-30)
        seasonal_factor = 1.0 + 0.25 * np.sin(2 * np.pi * (week_num - 10) / 52)
        
        # Holiday flag (major holiday weeks: New Year week 1, Easter week 15, Summer Fest week 28, Thanksgiving week 47, Xmas week 51)
        is_holiday = 1 if week_num in [1, 15, 28, 47, 51] and day_of_week in [4, 5, 6] else 0
        
        for store in stores:
            # Regional marketing spend ($50 - $400 daily)
            base_mkt = 150 * store_multiplier[store]
            marketing_spend = round(base_mkt + np.random.normal(0, 25) + (is_holiday * 80), 2)
            marketing_spend = max(20.0, marketing_spend)
            
            # Store customer footfall
            base_footfall = int(450 * store_multiplier[store] * seasonal_factor * (1.3 if is_weekend else 1.0))
            footfall = base_footfall + int(np.random.normal(0, 30)) + (100 if is_holiday else 0)
            footfall = max(50, footfall)

            for prod in products:
                prod_id = prod["id"]
                base_price = prod["base_price"]
                true_elasticity = prod["elasticity"]
                
                # Competitor pricing (tracks base price with market noise)
                comp_noise = np.random.normal(0, 0.08)
                competitor_price = round(base_price + comp_noise, 2)

                # Pricing policy:
                # Normal pricing: slight store-level random variation (+/- 3%)
                price_noise = np.random.normal(0, 0.05)
                unit_price = round(base_price + price_noise, 2)

                # TREATMENT INTERVENTION:
                # Store_1 undergoes dynamic price hike of +15% on PROD_101 starting at Week 36
                is_treatment_period = 1 if week_num >= 36 else 0
                is_treated_unit = 1 if store == "Store_1" else 0
                
                if is_treated_unit and prod_id == "PROD_101" and is_treatment_period:
                    # 15% price increase algorithm test
                    unit_price = round(base_price * 1.15 + np.random.normal(0, 0.04), 2)

                # Demand generation with microfoundations:
                # log(Q) = beta_0 + elasticity * log(P) + gamma * log(P_comp) + footfall_effect + mkt_effect + holiday_effect + noise
                price_ratio = unit_price / base_price
                comp_ratio = competitor_price / base_price
                
                # True underlying causal demand
                expected_units = (
                    80 * store_multiplier[store] * seasonal_factor
                    * (price_ratio ** true_elasticity)
                    * (comp_ratio ** 0.6)
                    * (1 + 0.15 * is_weekend)
                    * (1 + 0.25 * is_holiday)
                    * (1 + 0.0008 * (marketing_spend - 150))
                )
                
                # Realized quantity with Poisson-like variance
                units_sold = int(np.maximum(1, np.random.poisson(max(1.0, expected_units))))
                revenue = round(unit_price * units_sold, 2)
                
                tx_counter += 1
                records.append({
                    "transaction_id": f"TX_{tx_counter}",
                    "date": cur_date.strftime("%Y-%m-%d"),
                    "week": week_num,
                    "store_id": store,
                    "product_id": prod_id,
                    "product_name": prod["name"],
                    "unit_price": unit_price,
                    "units_sold": units_sold,
                    "revenue": revenue,
                    "competitor_price": competitor_price,
                    "marketing_spend": marketing_spend,
                    "store_footfall": footfall,
                    "is_holiday": is_holiday,
                    "is_weekend": is_weekend
                })

    df = pd.DataFrame(records)
    total_raw_rows = len(df)
    print(f"Base transaction rows generated: {total_raw_rows}")

    # -------------------------------------------------------------
    # Inject real-world data flaws for Member 1 to detect and clean:
    # -------------------------------------------------------------
    # 1. Duplicate records (~1.5% duplicates)
    dup_indices = np.random.choice(df.index, size=int(0.015 * len(df)), replace=False)
    df_duplicates = df.loc[dup_indices].copy()
    
    # 2. Missing values in non-critical columns (~2% nulls in competitor_price, ~1.5% in store_footfall)
    missing_comp_idx = np.random.choice(df.index, size=int(0.02 * len(df)), replace=False)
    df.loc[missing_comp_idx, "competitor_price"] = np.nan

    missing_footfall_idx = np.random.choice(df.index, size=int(0.015 * len(df)), replace=False)
    df.loc[missing_footfall_idx, "store_footfall"] = np.nan

    # 3. Invalid/Corrupt records (scan errors, negative returns, zero prices ~0.5%)
    corrupt_idx = np.random.choice(df.index, size=int(0.005 * len(df)), replace=False)
    for i, idx in enumerate(corrupt_idx):
        if i % 3 == 0:
            df.loc[idx, "unit_price"] = -df.loc[idx, "unit_price"]  # negative price error
        elif i % 3 == 1:
            df.loc[idx, "units_sold"] = -5  # return transaction / negative quantity
            df.loc[idx, "revenue"] = -5 * df.loc[idx, "unit_price"]
        else:
            df.loc[idx, "unit_price"] = 0.0  # free promotional glitch

    # Combine with duplicates and shuffle
    df_with_flaws = pd.concat([df, df_duplicates], ignore_index=True)
    df_with_flaws = df_with_flaws.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    
    return df_with_flaws

def get_project_root():
    curr = os.path.dirname(os.path.abspath(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "data")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

if __name__ == "__main__":
    root = get_project_root()
    output_dir = os.path.join(root, "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "retail_transactions_raw.csv")
    
    df_raw = generate_retail_data()
    df_raw.to_csv(output_path, index=False)
    print(f"Raw dataset generated and saved to: {output_path}")
    print(f"Total rows: {len(df_raw)}, Total columns: {len(df_raw.columns)}")
