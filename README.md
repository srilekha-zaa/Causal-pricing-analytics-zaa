# Causal Inference & Synthetic Control Engine for Algorithmic Pricing

An end-to-end econometric and machine learning engine to evaluate the true causal impact of algorithmic pricing changes on retail demand and revenue.

---

## 1. Project Overview & Workflow

This project compares:
1. **What actually happened** after an algorithmic price change.
2. **What would have happened** if the price change had never occurred (the **counterfactual**).

The difference between these two states is the **Causal Lift** ($\tau = Y(1) - Y(0)$).

```
   Raw Retail Transactions & Pricing Data
                   ↓
   Data Engineering & Panel Pipeline (Member 1)
         ↙                           ↘
Synthetic Control (Member 3)      Double ML (Member 4)
(Counterfactual prediction)     (Confounder adjustment)
         ↘                           ↙
   Causal DAG & Effect Evaluation (Member 2)
                   ↓
     Interactive Dashboard & Executive Report
```

---

## 2. Team Division & Module Responsibilities

| Role | Focus Area | Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Data Engineering** | Raw ingestion, cleaning pipeline, store/product/week panel, QA report, EDA charts | ✅ Complete |
| **Member 2** | **Causal Design & DAG** | DoWhy causal graph, treatment/control definitions, confounding structure | ⏳ In Progress |
| **Member 3** | **Synthetic Control** | Convex donor weights ($w_j$), counterfactual trajectory, placebo tests | ⏳ In Progress |
| **Member 4** | **Double ML & Dashboard** | Orthogonal ML elasticity ($\theta$), CATE, interactive Streamlit dashboard | ⏳ In Progress |

---

## 3. Member 1 Deliverables Summary

* **Raw Data:** `data/raw/retail_transactions_raw.csv` (11,083 transactions across 10 stores, 52 weeks).
* **Cleaning Pipeline:** `src/data_pipeline/clean_dataset.py` (drops duplicates, filters invalid prices/returns, imputes missing values).
* **Clean Data:** `data/processed/retail_transactions_cleaned.csv` (10,866 verified transactions).
* **Balanced Panel:** `data/processed/store_product_week_panel.csv` (1,560 rows: 10 stores $\times$ 3 products $\times$ 52 weeks).
* **QA Report:** `reports/data_quality_report.md`
* **Data Dictionary:** `reports/data_dictionary.md`
* **Team Handover Spec:** `reports/causal_setup_handover.md`
* **EDA Visualizations:** `reports/eda_figures/`
  * `01_price_trajectories_intervention.png`
  * `02_weekly_sales_volume_and_treatment.png`
  * `03_parallel_trends_validation.png`
  * `04_confounders_correlation_matrix.png`

---

## 4. Quick Start

### Run Member 1 Pipeline
To re-run the entire data engineering and visualization suite:
```bash
python run_member1_pipeline.py
```
