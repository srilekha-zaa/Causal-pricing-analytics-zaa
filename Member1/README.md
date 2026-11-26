# Member 1: Data Engineering & Common Pipeline
## Enterprise-Level Data Analytics Project — Algorithmic Pricing Engine

**Organization:** Zaalima Development — Enterprise Data Analytics  
**Author:** Samiksha Dewase (Member 1 Lead)  
**Downstream Deliverable For:** Member 2 (DAG), Member 3 (Synthetic Control), Member 4 (Double ML)

---

## 1. Overview & Responsibilities
As **Member 1**, this module owns the dataset collection, quality audit, preprocessing pipeline, and panel aggregation for the entire team.

### Deliverables Summary

| Deliverable | Description | File Location |
| :--- | :--- | :--- |
| **1. Raw Transaction Ingestion** | 52-week transaction dataset across 10 retail locations, including real-world noise, competitor shocks, ad spend, and holiday waves. | `data/raw/retail_transactions_raw.csv` |
| **2. Cleaning & QA Pipeline** | Deduplication, filtering negative returns/prices, and median imputation of missing confounder values. | `src/data_pipeline/clean_dataset.py`<br>`reports/data_quality_report.md` |
| **3. Cleaned Transactions** | 10,866 verified transaction records with 100% schema integrity. | `data/processed/retail_transactions_cleaned.csv` |
| **4. Balanced Longitudinal Panel** | 1,560 rows (10 stores × 3 products × 52 weeks) with causal indicators (`is_treated_store`, `is_post_treatment`, `treatment_active`). | `data/processed/store_product_week_panel.csv` |
| **5. Formatted Team Excel Workbook** | Multi-tab Excel file with freeze-panes, currency formats, conditional formatting, and pre-built SCM matrix. | `data/processed/store_product_week_panel.xlsx` |
| **6. Exploratory Data Analysis (EDA)** | 4 publication-quality charts validating the Week 36 intervention shock and pre-treatment parallel trends. | `reports/eda_figures/` |
| **7. Interactive Jupyter Notebook** | End-to-end data engineering notebook walkthrough. | `notebooks/01_member1_data_engineering.ipynb` |
| **8. Master Pipeline Runner** | One-command CLI runner executing the full data engineering pipeline. | `run_member1_pipeline.py` |

---

## 2. Quick Execution

To execute the entire Member 1 data pipeline:
```bash
python run_member1_pipeline.py
```

To run the interactive notebook:
```bash
jupyter notebook notebooks/01_member1_data_engineering.ipynb
```
