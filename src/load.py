
from pathlib import Path
from urllib.parse import quote_plus
from config import get_connection_string

import pandas as pd
from sqlalchemy import create_engine, text

# ============================================================
# RETAIL SALES ETL - TRANSACTIONAL LOAD
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Retrieve database configuration from .env
connection_string = get_connection_string()

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string),
    fast_executemany=True
)


def prepare_data(filename):
    """Read and prepare the transformed CSV data."""

    df = pd.read_csv(
        DATA_DIR / filename,
        dtype={
            "invoice_no": "string",
            "stock_code": "string",
            "description": "string",
            "country": "string"
        }
    )

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="raise"
    )

    df["customer_id"] = pd.to_numeric(
        df["customer_id"], errors="coerce"
    ).astype("Int64")

    return df


def load_data():
    """Refresh and validate both tables in one transaction."""

    print("Preparing data for SQL Server...")

    transactions = prepare_data(
        "retail_transactions_standardized.csv"
    )

    sales = prepare_data("retail_sales.csv")

    if transactions.empty or sales.empty:
        raise ValueError("Input dataset cannot be empty.")

    expected_valid_sales = int(
        transactions["is_valid_sale"].sum()
    )

    if expected_valid_sales != len(sales):
        raise ValueError(
            "Sales data does not match valid-sale flags."
        )

    print("Starting transactional data load...")

    # All database changes commit or roll back together.
    with engine.begin() as conn:

        # Clear existing records without dropping the tables.
        conn.execute(text(
            "DELETE FROM dbo.retail_sales"
        ))

        conn.execute(text(
            "DELETE FROM dbo.retail_transactions"
        ))

        # Load both datasets.
        datasets = {
            "retail_transactions": transactions,
            "retail_sales": sales
        }

        for table_name, df in datasets.items():

            print(f"Loading {table_name}...", flush=True)

            df.to_sql(
                name=table_name,
                con=conn,
                schema="dbo",
                if_exists="append",
                index=False,
                chunksize=1000
            )

            actual_count = conn.execute(
                text(
                    f"SELECT COUNT(*) FROM dbo.{table_name}"
                )
            ).scalar_one()

            print(
                f"{table_name}: "
                f"{actual_count:,} records loaded"
            )

            if actual_count != len(df):
                raise ValueError(
                    f"Record count mismatch in {table_name}"
                )

        # Validate sales classification.
        actual_valid_sales = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM dbo.retail_transactions
                WHERE is_valid_sale = 1
            """)
        ).scalar_one()

        if actual_valid_sales != len(sales):
            raise ValueError(
                "Sales classification validation failed."
            )

    # Reaching this point means the transaction committed.
    print("\nTransaction committed successfully!")
    print("Both SQL Server tables refreshed and validated.")


if __name__ == "__main__":
    try:
        load_data()

    except Exception:
        print("\nLoad failed. Transaction changes rolled back.")
        raise

    finally:
        engine.dispose()
