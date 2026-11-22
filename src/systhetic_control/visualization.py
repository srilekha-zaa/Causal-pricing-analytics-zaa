
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load Synthetic Control results
input_file = Path(
    "reports/synthetic_control/synthetic_control_results.csv"
)

df = pd.read_csv(input_file)

# Sort by week
df = df.sort_values("week")

# Create graph
plt.figure(figsize=(12, 6))

plt.plot(
    df["week"],
    df["actual_quantity"],
    label="Actual Store_1 Quantity",
    linewidth=2
)

plt.plot(
    df["week"],
    df["synthetic_quantity"],
    label="Synthetic Control Quantity",
    linewidth=2,
    linestyle="--"
)

# Mark intervention
plt.axvline(
    x=36,
    linestyle=":",
    label="Pricing Intervention (Week 36)"
)

plt.xlabel("Week")
plt.ylabel("Total Units Sold")

plt.title(
    "Actual vs Synthetic Control - Store_1 PROD_101"
)

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save graph
output_dir = Path("reports/synthetic_control")
output_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(
    output_dir / "synthetic_control.png",
    dpi=300
)

plt.show()

print("Graph saved successfully!")
