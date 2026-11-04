"""
Script: export_excel.py
Purpose: Converts store_product_week_panel.csv into a beautifully styled,
multi-tab Excel workbook for team distribution:
- Tab 1: Project Overview & Guide (Instructions for M2, M3, M4)
- Tab 2: Full Panel Data (with auto-filter, currency formatting, freeze pane, treatment highlight)
- Tab 3: SCM Pivot Matrix (Pre-formatted for Member 3 Synthetic Control)
- Tab 4: Store Summary Stats
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_styled_excel(csv_path, excel_path):
    print("Reading panel CSV:", csv_path)
    df = pd.read_csv(csv_path)

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styling Palettes
    navy_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    teal_header_fill = PatternFill(start_color="005B60", end_color="005B60", fill_type="solid")
    gold_header_fill = PatternFill(start_color="833C0C", end_color="833C0C", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    title_font = Font(name="Calibri", size=16, bold=True, color="1F4E79")
    subtitle_font = Font(name="Calibri", size=12, italic=True, color="595959")
    
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )
    
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    treatment_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # soft green
    treatment_font = Font(name="Calibri", size=11, bold=True, color="276A3C")

    # -------------------------------------------------------------
    # TAB 1: README & Guide
    # -------------------------------------------------------------
    ws_guide = wb.create_sheet(title="Guide & Team Setup")
    ws_guide.views.sheetView[0].showGridLines = True

    ws_guide["A1"] = "Algorithmic Pricing Analytics — Master Panel Dataset"
    ws_guide["A1"].font = title_font
    ws_guide["A2"] = "Prepared by Member 1 (Data Engineering) | Shared Master File for Members 2, 3, and 4"
    ws_guide["A2"].font = subtitle_font

    guide_rows = [
        ["", ""],
        ["1. QUICK PROJECT OVERVIEW", ""],
        ["Target Unit (Treated Store):", "Store_1 (Underwent algorithmic pricing test)"],
        ["Target Product:", "PROD_101 (Flagship Energy Drink 500ml)"],
        ["Intervention Week:", "Week 36 (Price increased by +15% from ~$3.50 to ~$4.02)"],
        ["Pre-treatment Window:", "Weeks 1 to 35 (Use this for donor weights & DAG baseline)"],
        ["Post-treatment Window:", "Weeks 36 to 52 (Use this for counterfactual lift & elasticity)"],
        ["Ground-truth Elasticity:", "-1.50 (True causal elasticity simulated for validation)"],
        ["", ""],
        ["2. HOW EACH TEAM MEMBER USES THIS FILE", ""],
        ["Member 2 (Causal Design & DAG):", "Use 'Panel Data (Full)'. Treatment = avg_unit_price, Outcome = total_units_sold, Confounders = avg_competitor_price, total_marketing_spend, avg_store_footfall, holiday_days."],
        ["Member 3 (Synthetic Control):", "Use 'SCM Matrix (PROD_101)'. It is already pre-pivoted into weeks x stores! Store_1 is treated, Store_2 to Store_10 are donors."],
        ["Member 4 (Double ML):", "Use 'Panel Data (Full)'. Treatment = log_price, Outcome = log_units, Confounders = [log_competitor_price, total_marketing_spend, avg_store_footfall, holiday_days]. Target: estimate theta ≈ -1.50."],
        ["", ""],
        ["3. COLUMN DEFINITIONS IN THE PANEL SHEET", ""],
        ["store_id", "Identifier for each store (Store_1 to Store_10)"],
        ["product_id", "Product SKU (PROD_101, PROD_102, PROD_103)"],
        ["week", "Week number of the year (1 to 52)"],
        ["avg_unit_price", "Average realized unit price during the week ($)"],
        ["total_units_sold", "Sum of units sold across the 7 days of the week"],
        ["total_revenue", "Total gross dollar sales ($)"],
        ["avg_competitor_price", "Average competitor shelf price during that week ($)"],
        ["total_marketing_spend", "Total localized ad spend ($)"],
        ["avg_store_footfall", "Average daily customer traffic in store"],
        ["holiday_days", "Count of holiday/promo days in that week"],
        ["is_treated_store", "1 if Store_1, else 0"],
        ["is_post_treatment", "1 if Week >= 36, else 0"],
        ["treatment_active", "1 ONLY for Store_1 on PROD_101 at Week >= 36 (Highlighted in Green)"],
        ["log_price / log_units", "Log transformations for Double ML elasticity estimation"]
    ]

    for r_idx, (col_a, col_b) in enumerate(guide_rows, start=3):
        ws_guide.cell(row=r_idx, column=1, value=col_a)
        ws_guide.cell(row=r_idx, column=2, value=col_b)
        if col_a.startswith(("1.", "2.", "3.")):
            ws_guide.cell(row=r_idx, column=1).font = bold_font
            ws_guide.cell(row=r_idx, column=1).fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
            ws_guide.cell(row=r_idx, column=2).fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        else:
            ws_guide.cell(row=r_idx, column=1).font = bold_font

    ws_guide.column_dimensions["A"].width = 30
    ws_guide.column_dimensions["B"].width = 95

    # -------------------------------------------------------------
    # TAB 2: Full Panel Data
    # -------------------------------------------------------------
    ws_panel = wb.create_sheet(title="Panel Data (Full)")
    ws_panel.views.sheetView[0].showGridLines = True
    ws_panel.freeze_panes = "A2"

    headers = list(df.columns)
    ws_panel.append(headers)

    # Header styling
    for col_idx in range(1, len(headers) + 1):
        cell = ws_panel.cell(row=1, column=col_idx)
        cell.fill = navy_header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Number format categories
    currency_cols = ["avg_unit_price", "weighted_unit_price", "total_revenue", "avg_competitor_price", "total_marketing_spend"]
    integer_cols = ["week", "total_units_sold", "avg_store_footfall", "holiday_days", "days_recorded", "is_treated_store", "is_post_treatment", "treatment_active"]
    decimal_cols = ["log_price", "log_units", "log_revenue", "log_competitor_price"]

    # Append data rows
    for r_idx, row_values in enumerate(df.values.tolist(), start=2):
        ws_panel.append(row_values)
        is_treated_active = (row_values[headers.index("treatment_active")] == 1)
        is_even = (r_idx % 2 == 0)

        for c_idx, val in enumerate(row_values, start=1):
            cell = ws_panel.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            col_name = headers[c_idx - 1]

            if is_treated_active:
                cell.fill = treatment_fill
                if col_name == "treatment_active":
                    cell.font = treatment_font
            elif is_even:
                cell.fill = zebra_fill

            # Apply formatting
            if col_name in currency_cols:
                cell.number_format = "$#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif col_name in integer_cols:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="center")
            elif col_name in decimal_cols:
                cell.number_format = "0.0000"
                cell.alignment = Alignment(horizontal="right")
            else:
                cell.alignment = Alignment(horizontal="left")

    # Auto-adjust column widths
    for col in ws_panel.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_panel.column_dimensions[col_letter].width = max(max_len + 3, 12)
    ws_panel.auto_filter.ref = ws_panel.dimensions

    # -------------------------------------------------------------
    # TAB 3: Pre-formatted Matrix for Member 3 (Synthetic Control)
    # -------------------------------------------------------------
    ws_scm = wb.create_sheet(title="SCM Matrix (PROD_101)")
    ws_scm.views.sheetView[0].showGridLines = True
    ws_scm.freeze_panes = "A3"

    df_p1 = df[df["product_id"] == "PROD_101"]
    scm_pivot = df_p1.pivot(index="week", columns="store_id", values="total_units_sold").reset_index()

    # Title Banner
    ws_scm.merge_cells("A1:K1")
    ws_scm["A1"] = "PROD_101 Weekly Units Sold Matrix (Rows: Weeks 1-52 | Columns: Treated Unit Store_1 & Donor Pool Store_2 to Store_10)"
    ws_scm["A1"].font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    ws_scm["A1"].fill = teal_header_fill
    ws_scm["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_scm.row_dimensions[1].height = 28

    scm_cols = ["week", "Store_1 (Treated)"] + [f"Store_{i} (Donor)" for i in range(2, 11)]
    ws_scm.append(scm_cols)

    for c_idx in range(1, len(scm_cols) + 1):
        cell = ws_scm.cell(row=2, column=c_idx)
        cell.fill = navy_header_fill if c_idx > 2 else (gold_header_fill if c_idx == 2 else teal_header_fill)
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    store_order = ["week", "Store_1"] + [f"Store_{i}" for i in range(2, 11)]
    for r_idx, row in scm_pivot.iterrows():
        week_num = int(row["week"])
        row_data = [week_num] + [int(row[s]) for s in store_order[1:]]
        ws_scm.append(row_data)
        excel_row = r_idx + 3
        is_post = (week_num >= 36)

        for c_idx in range(1, len(row_data) + 1):
            cell = ws_scm.cell(row=excel_row, column=c_idx)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center")
            cell.number_format = "#,##0"
            if is_post:
                if c_idx == 2:  # Treated post-treatment
                    cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # soft orange
                    cell.font = Font(name="Calibri", size=11, bold=True, color="C00000")
                else:
                    cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # light yellow post-treatment

    for col in ws_scm.columns:
        col_letter = get_column_letter(col[0].column)
        ws_scm.column_dimensions[col_letter].width = 18

    # -------------------------------------------------------------
    # TAB 4: Store Summary Stats
    # -------------------------------------------------------------
    ws_sum = wb.create_sheet(title="Store Summary Stats")
    ws_sum.views.sheetView[0].showGridLines = True
    
    summary_df = df.groupby("store_id").agg(
        avg_price=("avg_unit_price", "mean"),
        total_units=("total_units_sold", "sum"),
        total_revenue=("total_revenue", "sum"),
        avg_footfall=("avg_store_footfall", "mean"),
        total_marketing=("total_marketing_spend", "sum")
    ).reset_index()

    sum_headers = ["Store ID", "Avg Unit Price", "Total Units Sold", "Total Revenue", "Avg Daily Footfall", "Total Marketing Spend"]
    ws_sum.append(sum_headers)
    for c_idx in range(1, len(sum_headers) + 1):
        cell = ws_sum.cell(row=1, column=c_idx)
        cell.fill = navy_header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx, row in summary_df.iterrows():
        excel_row = r_idx + 2
        ws_sum.append([
            row["store_id"],
            round(row["avg_price"], 2),
            int(row["total_units"]),
            round(row["total_revenue"], 2),
            round(row["avg_footfall"], 1),
            round(row["total_marketing"], 2)
        ])
        for c_idx in range(1, len(sum_headers) + 1):
            cell = ws_sum.cell(row=excel_row, column=c_idx)
            cell.border = thin_border
            if c_idx in [2, 4, 6]:
                cell.number_format = "$#,##0.00"
                cell.alignment = Alignment(horizontal="right")
            elif c_idx in [3, 5]:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="center")

    for col in ws_sum.columns:
        col_letter = get_column_letter(col[0].column)
        ws_sum.column_dimensions[col_letter].width = 22

    # Save Excel workbook
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    wb.save(excel_path)
    print(f"Excel workbook created successfully at: {excel_path}")

if __name__ == "__main__":
    csv_in = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\processed\store_product_week_panel.csv"
    xlsx_out = r"C:\Users\ACER\.gemini\antigravity\scratch\causal-pricing-engine\data\processed\store_product_week_panel.xlsx"

    create_styled_excel(csv_in, xlsx_out)
