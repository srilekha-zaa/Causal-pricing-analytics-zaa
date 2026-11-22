
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from pathlib import Path

# Project configuration
TREATED_STORE = "Store_1"
PRODUCT = "PROD_101"

DONOR_STORES = [
    f"Store_{i}" for i in range(2, 11)
]

PRE_WEEKS = range(1, 36)
POST_WEEKS = range(36, 53)

DATA_PATH = Path(
    "data/processed/store_product_week_panel.csv"
)


def load_data():

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Columns:", df.columns.tolist())

    return df


def prepare_data(df):

    # Filter selected product
    df = df[df["product_id"] == PRODUCT].copy()

    # Check required columns
    required = [
        "store_id",
        "week",
        "total_units_sold"
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Create store vs week matrix
    panel = df.pivot_table(
        index="week",
        columns="store_id",
        values="total_units_sold",
        aggfunc="sum"
    ).sort_index()

    stores = [TREATED_STORE] + DONOR_STORES

    missing_stores = [
        store for store in stores
        if store not in panel.columns
    ]

    if missing_stores:
        raise ValueError(
            f"Missing stores: {missing_stores}"
        )

    panel = panel[stores]

    if panel.isnull().any().any():
        raise ValueError(
            "Missing store-week observations. "
            "Check the panel before fitting."
        )

    return panel


def calculate_weights(treated, donors):

    X = donors.loc[list(PRE_WEEKS)].values
    y = treated.loc[list(PRE_WEEKS)].values

    n = X.shape[1]

    def objective(weights):
        prediction = X @ weights
        return np.mean((y - prediction) ** 2)

    result = minimize(
        objective,
        x0=np.ones(n) / n,
        method="SLSQP",
        bounds=[(0, 1)] * n,
        constraints={
            "type": "eq",
            "fun": lambda w: np.sum(w) - 1
        }
    )

    if not result.success:
        raise RuntimeError(result.message)

    return pd.Series(
        result.x,
        index=donors.columns,
        name="weight"
    )


def main():

    df = load_data()

    panel = prepare_data(df)

    treated = panel[TREATED_STORE]
    donors = panel[DONOR_STORES]

    weights = calculate_weights(
        treated,
        donors
    )

    synthetic = donors @ weights

    pre_mspe = np.mean(
        (
            treated.loc[list(PRE_WEEKS)]
            - synthetic.loc[list(PRE_WEEKS)]
        ) ** 2
    )

    results = pd.DataFrame({
        "week": panel.index,
        "actual_quantity": treated.values,
        "synthetic_quantity": synthetic.values
    })

    results["impact"] = (
        results["actual_quantity"]
        - results["synthetic_quantity"]
    )

    print("\nDONOR WEIGHTS")
    print(weights)

    print("\nPRE-TREATMENT MSPE:", pre_mspe)

    print("\nPOST-TREATMENT IMPACT")
    print(
        results[
            results["week"].isin(POST_WEEKS)
        ]["impact"].mean()
    )

    output_dir = Path("reports/synthetic_control")
    output_dir.mkdir(parents=True, exist_ok=True)

    weights.to_csv(output_dir / "donor_weights.csv")

    results.to_csv(
        output_dir / "synthetic_control_results.csv",
        index=False
    )

    print("\nResults saved successfully!")


if __name__ == "__main__":
    main()
