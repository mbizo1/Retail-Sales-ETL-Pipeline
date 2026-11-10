
from pathlib import Path
import pandas as pd

# ============================================================
# RETAIL SALES ETL - TRANSFORM STAGE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Starting data transformation...")

# 1. Load source data
df = pd.read_excel(RAW_FILE, engine="openpyxl")

print(f"Source records: {len(df):,}")

# 2. Standardise column names
df = df.rename(columns={
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country"
})

# 3. Standardise data types
df["invoice_no"] = df["invoice_no"].astype("string").str.strip()
df["stock_code"] = df["stock_code"].astype("string").str.strip()
df["description"] = df["description"].astype("string").str.strip()
df["country"] = df["country"].astype("string").str.strip()

df["invoice_date"] = pd.to_datetime(
    df["invoice_date"], errors="coerce"
)

df["quantity"] = pd.to_numeric(
    df["quantity"], errors="coerce"
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"], errors="coerce"
)

# 4. Identify duplicate records
df["is_duplicate"] = df.duplicated()

# 5. Identify cancellations and questionable transactions
df["is_cancellation"] = (
    df["invoice_no"].str.upper().str.startswith("C", na=False)
)

df["is_nonpositive_quantity"] = df["quantity"] <= 0
df["is_nonpositive_price"] = df["unit_price"] <= 0

# 6. Calculate transaction line amounts
df["line_total"] = df["quantity"] * df["unit_price"]

# 7. Identify valid positive sales
df["is_valid_sale"] = (
    (~df["is_cancellation"])
    & (df["quantity"] > 0)
    & (df["unit_price"] > 0)
)

# 8. Create the sales-only dataset
sales_df = df.loc[df["is_valid_sale"]].copy()

# 9. Export transformed records
df.to_csv(
    OUTPUT_DIR / "retail_transactions_standardized.csv",
    index=False
)

sales_df.to_csv(
    OUTPUT_DIR / "retail_sales.csv",
    index=False
)

# 10. Display transformation summary
print("\n--- TRANSFORMATION SUMMARY ---")

print(f"Original records: {len(df):,}")
print(f"Valid positive sales: {len(sales_df):,}")
print(f"Other records: {len(df) - len(sales_df):,}")
print(f"Duplicates flagged: {df['is_duplicate'].sum():,}")
print(f"Cancellations flagged: {df['is_cancellation'].sum():,}")

print("\nTransformation completed successfully!")
