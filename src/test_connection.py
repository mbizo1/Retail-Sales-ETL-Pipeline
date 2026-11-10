
import pyodbc
from config import get_connection_string

print("Testing SQL Server configuration...")

try:
    conn = pyodbc.connect(
        get_connection_string(),
        timeout=10
    )

    cursor = conn.cursor()
    cursor.execute("SELECT DB_NAME()")

    database = cursor.fetchone()[0]

    print("Connection successful!")
    print("Connected database:", database)

    conn.close()

except pyodbc.Error as error:
    print("Connection failed:")
    print(error)
    raise
