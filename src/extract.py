
from pathlib import Path
import pandas as pd

# Locate the project root and source file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FILE_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"

# Extract the retail sales dataset
print("Starting data extraction...")

df = pd.read_excel(FILE_PATH, engine="openpyxl")

# Inspect the extracted data
print("\nTotal records:", len(df))

print("\nDataset columns:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nData extraction completed successfully!")


# ============================================================
# DATA QUALITY ASSESSMENT
# ============================================================

print("\n--- DATA QUALITY REPORT ---")

# Check missing values
print("\nMissing values by column:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate records:")
print(df.duplicated().sum())

# Check invalid quantities
print("\nTransactions with zero or negative quantity:")
print((df["Quantity"] <= 0).sum())

# Check invalid prices
print("\nTransactions with zero or negative unit price:")
print((df["UnitPrice"] <= 0).sum())

# Check cancellation invoices
print("\nCancellation invoice records:")
print(
    df["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
    .sum()
)
