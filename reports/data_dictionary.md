# Data Dictionary: Algorithmic Pricing & Causal Inference

This document details all columns present in the raw transactional dataset (`retail_transactions_raw.csv`), cleaned dataset (`retail_transactions_cleaned.csv`), and the aggregated panel dataset (`store_product_week_panel.csv`).

---

## 1. Cleaned Transaction Dataset (`retail_transactions_cleaned.csv`)

| Column Name | Data Type | Units / Range | Description | Role in Causal System |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | String | e.g. `TX_1000001` | Unique transaction identifier | Index / Audit key |
| `date` | Date | `2025-01-01` to `2025-12-31` | Date of purchase | Time coordinate |
| `week` | Integer | `1` to `52` | Calendar week number of the year | Time coordinate / aggregation |
| `store_id` | String | `Store_1` to `Store_10` | Unique store location code | Unit identifier |
| `product_id` | String | `PROD_101` to `PROD_103` | Unique SKU identifier | Sub-unit identifier |
| `product_name` | String | Text | Descriptive item title | Reference |
| `unit_price` | Float | `$1.50` to `$4.20` | Realized retail shelf price | **Treatment variable ($T$)** |
| `units_sold` | Integer | `1` to `180` | Quantity purchased in transaction | **Outcome variable ($Y$)** |
| `revenue` | Float | `unit_price * units_sold` | Gross dollar sales | Secondary outcome |
| `competitor_price`| Float | `$1.60` to `$4.10` | Competitor shelf price within 2 miles | **Confounder ($X_1$)** |
| `marketing_spend` | Float | `$20.00` to `$500.00` | Daily localized digital/print ad spend | **Confounder ($X_2$)** |
| `store_footfall`  | Integer | `50` to `800` | Daily foot traffic in the store | **Confounder ($X_3$)** |
| `is_holiday`      | Binary | `0` or `1` | Indicator for retail promotional holidays | **Confounder ($X_4$)** |
| `is_weekend`      | Binary | `0` or `1` | Saturday / Sunday flag | Demand seasonality control |

---

## 2. Store-Product-Week Panel Dataset (`store_product_week_panel.csv`)

This is the primary panel dataset ingested by **Member 2 (DAG)**, **Member 3 (Synthetic Control)**, and **Member 4 (Double ML)**.

| Column Name | Data Type | Description | Intended Usage |
| :--- | :--- | :--- | :--- |
| `store_id` | String | Store code (`Store_1` ... `Store_10`) | Unit cross-section dimension |
| `product_id` | String | Product SKU | Stratification dimension |
| `week` | Integer | Week index (1 to 52) | Longitudinal time dimension |
| `avg_unit_price` | Float | Weekly average shelf price | Treatment variable for DML |
| `weighted_unit_price` | Float | Revenue-weighted average price | Robustness check price |
| `total_units_sold` | Integer | Total units sold across all 7 days | Primary outcome variable ($Y$) |
| `total_revenue` | Float | Total gross dollar sales | Business impact metric |
| `avg_competitor_price` | Float | Average competitor price that week | Price elasticity baseline |
| `total_marketing_spend`| Float | Sum of ad spend for the week | Exogenous demand shifter |
| `avg_store_footfall` | Float | Average daily store visitors | Proxy for store baseline volume |
| `holiday_days` | Integer | Number of holiday days in the week | Demand shock adjuster |
| `is_treated_store` | Binary | `1` if `store_id == "Store_1"` else `0` | Identifies treated entity |
| `is_post_treatment` | Binary | `1` if `week >= 36` else `0` | Identifies post-intervention window |
| `treatment_active` | Binary | `1` for `Store_1` on `PROD_101` at `week >= 36` | Interaction treatment dummy |
| `log_price` | Float | $\ln(\text{avg\_unit\_price})$ | Standard log-log demand elasticity |
| `log_units` | Float | $\ln(\text{total\_units\_sold})$ | Standard log-log demand elasticity |
| `log_revenue` | Float | $\ln(\text{total\_revenue})$ | Revenue elasticity |
| `log_competitor_price`| Float | $\ln(\text{avg\_competitor\_price})$ | Cross-price elasticity control |
