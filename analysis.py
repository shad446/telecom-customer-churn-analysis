
import pandas as pd
from pathlib import Path

# Find the CSV file in this project folder
csv_files = list(Path(".").glob("*.csv"))

if not csv_files:
    print("No CSV file found. Put your dataset in this folder.")
else:
    file_path = csv_files[0]
    df = pd.read_csv(file_path)

    print("Dataset loaded successfully!")
    print("File:", file_path.name)
    print("Dataset shape:", df.shape)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

# 1. Customer churn analysis
print("\n========== CUSTOMER CHURN ANALYSIS ==========")

print("\nChurn counts:")
print(df["Churn"].value_counts())

print("\nChurn percentages:")
print((df["Churn"].value_counts(normalize=True) * 100).round(2))

total_customers = len(df)
churned_customers = (df["Churn"] == "Yes").sum()
retained_customers = (df["Churn"] == "No").sum()
churn_rate = (churned_customers / total_customers) * 100

print("\nTotal customers:", total_customers)
print("Customers who churned:", churned_customers)
print("Customers retained:", retained_customers)
print(f"Overall churn rate: {churn_rate:.2f}%")

# 2. Churn by contract type
print("\n========== CHURN BY CONTRACT TYPE ==========")

contract_churn = df.groupby("Contract")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).round(2)

print("\nChurn rate by contract type (%):")
print(contract_churn.sort_values(ascending=False))

# 3. Churn by monthly charges
print("\n========== CHURN BY MONTHLY CHARGES ==========")

df["MonthlyChargesGroup"] = pd.cut(
    df["MonthlyCharges"],
    bins=[0, 30, 60, 90, 120],
    labels=["0–30", "31–60", "61–90", "91–120"],
    include_lowest=True
)

charges_churn = df.groupby(
    "MonthlyChargesGroup", observed=False
)["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).round(2)

print("\nChurn rate by monthly charges (%):")
print(charges_churn)

# 4. Churn by customer tenure
print("\n========== CHURN BY TENURE ==========")

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 60, 72],
    labels=[
        "0–12 months",
        "13–24 months",
        "25–48 months",
        "49–60 months",
        "61–72 months"
    ]
)

tenure_churn = df.groupby(
    "TenureGroup", observed=False
)["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).round(2)

print("\nChurn rate by tenure (%):")
print(tenure_churn)

import matplotlib.pyplot as plt

# Churn rate by contract type
contract_churn = df.groupby("Contract")["Churn"].apply(
    lambda x: (x == "Yes").mean() * 100
).sort_values(ascending=False)

plt.figure(figsize=(8, 5))
bars = plt.bar(contract_churn.index, contract_churn.values)

plt.title("Customer Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.1f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("churn_by_contract.png", dpi=300)
plt.show()

print("Chart saved as churn_by_contract.png")

# Churn analysis by internet service
print("\n========== CHURN BY INTERNET SERVICE ==========")

internet_churn = (
    df.groupby("InternetService")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values(ascending=False)
    .round(2)
)

print("\nChurn rate by internet service (%):")
print(internet_churn)

# Create and save the chart
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
bars = plt.bar(internet_churn.index, internet_churn.values)

plt.title("Customer Churn Rate by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Churn Rate (%)")

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.1f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("churn_by_internet_service.png", dpi=300)
plt.close()

print("Chart saved: churn_by_internet_service.png")

# Churn Analysis by Payment Method

payment_churn = df.groupby("PaymentMethod")["Churn"].value_counts(
    normalize=True
).unstack(fill_value=0) * 100

print("\nChurn Analysis by Payment Method:")
print(payment_churn.round(2))

import matplotlib.pyplot as plt
import seaborn as sns

# Calculate churn percentage by payment method
payment_churn = (
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values(ascending=False)
)

# Create a professional chart
plt.figure(figsize=(10, 6))
sns.barplot(
    x=payment_churn.values,
    y=payment_churn.index
)

plt.title("Customer Churn Rate by Payment Method",
          fontsize=16, fontweight="bold")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Payment Method")
plt.xlim(0, 100)
plt.tight_layout()
plt.show()

# Churn Analysis by Internet Service

internet_churn = (
    df.groupby("InternetService")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .sort_values(ascending=False)
)

print("\nChurn Rate by Internet Service:")
print(internet_churn.round(2))

# Professional visualization
plt.figure(figsize=(10, 6))

bars = plt.bar(
    internet_churn.index,
    internet_churn.values
)

plt.title(
    "Customer Churn Rate by Internet Service",
    fontsize=16,
    fontweight="bold"
)
plt.xlabel("Internet Service")
plt.ylabel("Churn Rate (%)")
plt.ylim(0, 100)

# Add percentage labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.1f}%",
        ha="center",
        fontsize=11
    )

plt.tight_layout()
plt.show()

# Customer Churn by Tenure

df["tenure_group"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=[
        "0-12 Months",
        "13-24 Months",
        "25-48 Months",
        "49-72 Months"
    ]
)

tenure_churn = (
    df.groupby("tenure_group", observed=False)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

print("\nChurn Rate by Customer Tenure:")
print(tenure_churn.round(2))

# Professional visualization
plt.figure(figsize=(10, 6))

bars = plt.bar(
    tenure_churn.index.astype(str),
    tenure_churn.values
)

plt.title(
    "Customer Churn Rate by Tenure",
    fontsize=16,
    fontweight="bold"
)
plt.xlabel("Customer Tenure")
plt.ylabel("Churn Rate (%)")
plt.ylim(0, 100)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.1f}%",
        ha="center",
        fontsize=10
    )

plt.tight_layout()
plt.show()

# Churn Analysis by Monthly Charges

df["Churn_Status"] = df["Churn"].map({
    "Yes": "Churned",
    "No": "Stayed"
})

charge_analysis = (
    df.groupby("Churn_Status")["MonthlyCharges"]
    .agg(["mean", "median", "count"])
    .round(2)
)

print("\nMonthly Charges Analysis:")
print(charge_analysis)

# Professional visualization
plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Churn_Status",
    y="MonthlyCharges",
    hue="Churn_Status",
    palette={
        "Churned": "#D6B875",
        "Stayed": "#78A6A3"
    },
    legend=False
)

plt.title(
    "Monthly Charges: Churned vs Stayed Customers",
    fontsize=15,
    fontweight="bold"
)
plt.xlabel("Customer Status")
plt.ylabel("Monthly Charges ($)")
plt.tight_layout()
plt.show()

# BUSINESS ANALYSIS SUMMARY

print("\n" + "=" * 45)
print("TELECOM CUSTOMER CHURN: BUSINESS SUMMARY")
print("=" * 45)

total = len(df)
churned = df["Churn"].eq("Yes").sum()

print(f"\nTotal customers: {total:,}")
print(f"Churned customers: {churned:,}")
print(f"Retained customers: {total - churned:,}")
print(f"Overall churn rate: {churned / total * 100:.2f}%")

print("\n--- Churn by Contract ---")
print(
    df.groupby("Contract")["Churn"]
    .apply(lambda s: (s == "Yes").mean() * 100)
    .round(2)
    .sort_values(ascending=False)
)

print("\n--- Churn by Internet Service ---")
print(
    df.groupby("InternetService")["Churn"]
    .apply(lambda s: (s == "Yes").mean() * 100)
    .round(2)
    .sort_values(ascending=False)
)

print("\n--- Churn by Payment Method ---")
print(
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda s: (s == "Yes").mean() * 100)
    .round(2)
    .sort_values(ascending=False)
)

print("\n--- Monthly Charges Comparison ---")
print(
    df.groupby("Churn")["MonthlyCharges"]
    .agg(["mean", "median", "count"])
    .round(2)
)

print("\n--- Tenure Comparison ---")
print(
    df.groupby("Churn")["tenure"]
    .agg(["mean", "median", "count"])
    .round(2)
)

print("\nBUSINESS SUMMARY COMPLETE")
