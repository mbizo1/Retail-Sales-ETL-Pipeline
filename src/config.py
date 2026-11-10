
from pathlib import Path
import os
from dotenv import load_dotenv

# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

SERVER = os.getenv("SQL_SERVER")
DATABASE = os.getenv("SQL_DATABASE")
DRIVER = os.getenv("SQL_ODBC_DRIVER")

def get_connection_string():
    """Build the SQL Server connection string."""

    if not all([SERVER, DATABASE, DRIVER]):
        raise ValueError(
            "Missing SQL Server settings in .env"
        )

    return (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
    )
