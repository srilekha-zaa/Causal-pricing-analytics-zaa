# Causal Inference & Synthetic Control Engine for Algorithmic Pricing
## Enterprise-Level Data Analytics Project

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Causal Framework](https://img.shields.io/badge/Causal%20Framework-DoWhy%20%7C%20NetworkX%20%7C%20EconML-emerald.svg)](https://github.com/py-why/dowhy)
[![Dashboard](https://img.shields.io/badge/UI-Streamlit%20Interactive%20Dashboard-red.svg)](https://streamlit.io/)

An end-to-end econometric and causal machine learning engine to evaluate the true causal impact of algorithmic pricing changes on retail demand and revenue.

---

## 👥 Team Division & Module Responsibilities

* **Organization:** Zaalima Development — Enterprise Data Analytics

| Role | Contributor | Focus Area | Status |
| :--- | :--- | :--- | :---: |
| **Member 1** | **Samiksha Dewase** | **Data Engineering, Balanced Store-Product-Week Panel, QA & EDA** | ✅ **Complete** |
| **Member 2** | **Srilekha** | **Causal Design, Structural DAG & DoWhy Backdoor Identification** | ✅ **Complete** |
| **Member 3** | Omkar Jasud | Synthetic Control Method (SCM) & Donor Pool Weights | ⏳ In Progress |
| **Member 4** | **Riyaz M** | **Double Machine Learning (DML), CATE & Interactive Streamlit Dashboard** | ✅ **Complete** |

---

## 📊 Member 1 Deliverables Summary (`Samiksha Dewase`)

| Deliverable | Description | File Location |
| :--- | :--- | :--- |
| **1. Raw Transaction Ingestion** | 52-week transaction dataset across 10 retail locations, including real-world noise, competitor shocks, ad spend, and holiday waves. | `data/raw/retail_transactions_raw.csv` |
| **2. Cleaning & QA Pipeline** | Deduplication, filtering negative returns/prices, and median imputation of missing confounder values. | `src/data_pipeline/clean_dataset.py`<br>`reports/data_quality_report.md` |
| **3. Cleaned Transactions** | 10,866 verified transaction records with 100% schema integrity. | `data/processed/retail_transactions_cleaned.csv` |
| **4. Balanced Longitudinal Panel** | 1,560 rows (10 stores × 3 products × 52 weeks) with causal indicators (`is_treated_store`, `is_post_treatment`, `treatment_active`). | `data/processed/store_product_week_panel.csv` |
| **5. Master Excel Workbook** | Multi-tab Excel file with freeze-panes, currency formats, conditional formatting, and pre-built SCM matrix. | `data/processed/store_product_week_panel.xlsx` |
| **6. Visual EDA Figures** | 4 publication-quality charts validating the Week 36 intervention shock and pre-treatment parallel trends. | `reports/eda_figures/` |
| **7. Interactive Notebook** | Jupyter walkthrough of ingestion, cleaning, panel build, and EDA. | `notebooks/01_member1_data_engineering.ipynb` |
| **8. Dedicated Workspace** | Dedicated Member 1 folder containing all scripts, notebook, reports, and runner. | `Member1/` |
| **9. Master Pipeline Runner** | CLI master runner script verifying the entire Member 1 data pipeline. | `run_member1_pipeline.py` |

---

## 📌 Member 2 Deliverables Summary (`Srilekha`)

| Deliverable | Description | File Location |
| :--- | :--- | :--- |
| **1. Causal Research Design** | Formal potential outcomes framing, potential estimands (ATT & elasticity $\eta$), mathematical identification assumptions. | `docs/causal_research_design.md` |
| **2. Treatment & Control Specs** | Formal unit boundaries: **Treated Unit** (`Store_1` on `PROD_101`) vs **Donor Pool** (`Store_2`–`Store_10`), pre-treatment baseline vs post-treatment intervention. | `docs/treatment_control_specification.md` |
| **3. Confounder Matrix & Bad Controls** | Confounder taxonomy: competitor telemetry, ad spend, footfall, holiday shocks. Detailed analysis of **Bad Controls** (mediators and colliders). | `docs/confounder_documentation.md` |
| **4. Structural Causal DAG** | NetworkX structural causal graph module with automated DOT generation for DoWhy and visual plot. | `src/causal_design/dag_builder.py` |
| **5. DoWhy Identification Engine** | Microsoft DoWhy pipeline implementing Pearl's Backdoor Criterion, initial elasticity estimation, and 3 sensitivity refuters. | `src/causal_design/dowhy_identifier.py` |
| **6. Visual DAG & Diagnostics** | Publication-grade plots showing the color-coded DAG structure and refutation sensitivity diagnostics. | `reports/causal_figures/05_causal_dag_structure.png`<br>`reports/causal_figures/06_refutation_diagnostics.png` |
| **7. Interactive Walkthrough Notebook** | Step-by-step Jupyter notebook covering data ingestion, treatment split, DAG plotting, and DoWhy refutation checks. | `notebooks/02_member2_causal_design_and_dag.ipynb` |
| **8. Master Pipeline Runner** | CLI master runner script that verifies the full Member 2 pipeline. | `run_member2_causal_design.py` |

---

## 📈 Member 4 Deliverables Summary (`Riyaz M`)

| Deliverable | Description | File Location |
| :--- | :--- | :--- |
| **1. Double ML Engine** | 5-fold cross-fitted Partialling-Out Double ML (`RandomForest`, `GradientBoosting`, `Ridge`), CATE segmentation, and counterfactual lift calculator. | `src/dml/double_ml_engine.py` |
| **2. DML Diagnostic Plots** | Publication-grade benchmark forest plot, orthogonalized residual regression fit, CATE heterogeneity chart, and counterfactual demand/revenue trajectory. | `src/dml/dml_visualizations.py`<br>`reports/dml_figures/` |
| **3. Master DML Runner** | Single-command CLI script executing the full Member 4 estimation, CATE, counterfactual, and plotting pipeline. | `run_member4_dml_pipeline.py` |
| **4. Interactive Dashboard** | 4-tab Streamlit executive dashboard with KPI cards, estimator comparison, CATE explorer, and interactive what-if price simulator. | `app.py` |
| **5. Technical Report & Outputs** | Econometric writeup, JSON summary, model comparison CSV, CATE CSV, orthogonal residuals CSV, and Store_1 counterfactual CSV. | `docs/member4_dml_report.md`<br>`reports/dml_results/` |

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Execute Member 1 Pipeline (Data Engineering)
```bash
python run_member1_pipeline.py
```

### 3. Execute Member 2 Pipeline (Causal Design & DAG)
```bash
python run_member2_causal_design.py
```

### 4. Execute Member 4 Pipeline (Double Machine Learning)
```bash
python run_member4_dml_pipeline.py
```

### 5. Launch Interactive Executive Dashboard
```bash
streamlit run app.py
```

### 6. Open Interactive Jupyter Walkthroughs
```bash
jupyter notebook notebooks/01_member1_data_engineering.ipynb
jupyter notebook notebooks/02_member2_causal_design_and_dag.ipynb
```
