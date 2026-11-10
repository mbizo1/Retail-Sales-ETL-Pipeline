
from pathlib import Path
import pandas as pd
import pyodbc
from config import get_connection_string

# ============================================================
# RETAIL SALES ETL - VALIDATION STAGE
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Retrieve database configuration from .env
connection_string = get_connection_string()

print("Starting ETL validation...")

# 1. Get expected record counts from processed files

transactions = pd.read_csv(
    DATA_DIR / "retail_transactions_standardized.csv",
    usecols=["is_valid_sale"]
)

sales = pd.read_csv(
    DATA_DIR / "retail_sales.csv",
    usecols=["invoice_no"]
)

expected_transactions = len(transactions)
expected_sales = len(sales)
expected_valid_sales = int(transactions["is_valid_sale"].sum())

# 2. Check records loaded into SQL Server

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.retail_transactions"
    )
    actual_transactions = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM dbo.retail_sales"
    )
    actual_sales = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM dbo.retail_transactions
        WHERE is_valid_sale = 1
    """)
    actual_valid_sales = cursor.fetchone()[0]

# 3. Print validation results

print("\n--- ETL VALIDATION REPORT ---")

print(f"Expected transactions: {expected_transactions:,}")
print(f"Loaded transactions:   {actual_transactions:,}")

print(f"\nExpected sales:        {expected_sales:,}")
print(f"Loaded sales:          {actual_sales:,}")

print(f"\nExpected valid flags:  {expected_valid_sales:,}")
print(f"Loaded valid flags:    {actual_valid_sales:,}")

# 4. Validate the results

assert actual_transactions == expected_transactions, \
    "Transaction count mismatch!"

assert actual_sales == expected_sales, \
    "Sales count mismatch!"

assert actual_valid_sales == expected_valid_sales, \
    "Valid-sales flag count mismatch!"

assert actual_sales == actual_valid_sales, \
    "Sales table and transaction flags do not match!"

print("\nALL VALIDATION CHECKS PASSED!")
