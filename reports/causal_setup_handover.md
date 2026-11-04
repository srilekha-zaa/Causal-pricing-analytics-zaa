# Causal Study Setup & Team Handover Specification

This document defines the formal causal research setup prepared by **Member 1 (Data Engineering)** for **Member 2 (Causal Design & DAG)**, **Member 3 (Synthetic Control)**, and **Member 4 (Double ML & Integration)**.

---

## 1. Causal Intervention & Unit Definitions

* **Target Unit (Treated Entity):** `Store_1`
* **Target Product:** `PROD_101` (Flagship Energy Drink 500ml)
* **Donor Pool (Control Entities):** `Store_2`, `Store_3`, `Store_4`, `Store_5`, `Store_6`, `Store_7`, `Store_8`, `Store_9`, `Store_10` (9 unshocked stores).
* **Pre-Treatment Period:** Weeks `1` through `35` (35 weeks baseline).
* **Post-Treatment Period:** Weeks `36` through `52` (17 weeks intervention window).
* **Treatment Intervention:** Starting at Week 36, `Store_1` initiated an algorithmic pricing experiment, increasing unit price by **+15%** (from ~$3.50 to ~$4.02).

---

## 2. Ground-Truth Economic Parameters (For Model Evaluation)

Because Member 1 generated this environment with econometric microfoundations, we have known ground-truth parameters to benchmark the accuracy of Member 3 and Member 4's models:

| Parameter | Ground Truth Value | Definition |
| :--- | :--- | :--- |
| **True Own-Price Elasticity ($\eta$)** | **$-1.50$** | $\frac{\%\Delta \text{Quantity}}{\%\Delta \text{Price}}$ |
| **True Cross-Price Elasticity** | **$+0.60$** | Demand shift relative to competitor price |
| **Intervention Price Jump** | **$+15.0\%$** | Price hike on PROD_101 in Store_1 |
| **Expected Causal Quantity Drop** | **$\approx -22.5\%$** | $(-1.50 \times 15.0\%)$ drop vs counterfactual |

---

## 3. How Teammates Ingest the Data

### For Member 2 (Causal Design & DAG)
* Input file: `data/processed/store_product_week_panel.csv`
* Treatment variable: `avg_unit_price` (continuous) or `treatment_active` (binary).
* Outcome variable: `total_units_sold` or `log_units`.
* Confounders to include in DAG: `avg_competitor_price`, `total_marketing_spend`, `avg_store_footfall`, `holiday_days`.

### For Member 3 (Synthetic Control)
* Input file: `data/processed/store_product_week_panel.csv` filtered on `product_id == 'PROD_101'`.
* Pivot table structure:
  ```python
  import pandas as pd
  df = pd.read_csv("data/processed/store_product_week_panel.csv")
  df_p1 = df[df["product_id"] == "PROD_101"]
  Y_matrix = df_p1.pivot(index="week", columns="store_id", values="total_units_sold")
  # Treated column: Y_matrix["Store_1"]
  # Donor pool: Y_matrix[["Store_2", ..., "Store_10"]]
  # Pre-treatment rows: index 1 to 35
  # Post-treatment rows: index 36 to 52
  ```

### For Member 4 (Double ML)
* Input file: `data/processed/store_product_week_panel.csv`
* Outcome ($Y$): `log_units`
* Treatment ($T$): `log_price`
* Confounders ($X$): `['log_competitor_price', 'total_marketing_spend', 'avg_store_footfall', 'holiday_days']`
* Double ML objective: Residualize $Y$ and $T$ using LightGBM/Random Forest, then compute orthogonalized $\hat{\theta} \approx -1.50$.
