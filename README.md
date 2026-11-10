# Retail Sales ETL Pipeline Using Python and SQL Server

## Project Overview

This project implements an end-to-end Extract, Transform, Load (ETL) pipeline using Python and Microsoft SQL Server.

The pipeline processes historical retail transaction data, performs data quality checks, transforms raw records into structured datasets, and loads the results into SQL Server for analysis.

It demonstrates practical data engineering concepts including ETL development, database integration, automated validation, error handling, logging, transactional loading, and repeatable execution.

## Technologies Used

- **Python:** ETL development and automation
- **Pandas:** Data extraction, cleaning and transformation
- **SQL Server:** Relational database storage
- **SQLAlchemy and pyodbc:** Python-to-SQL Server integration
- **openpyxl:** Excel file processing
- **python-dotenv:** Environment configuration
- **SQL Server Management Studio:** Database validation and analysis
- **Visual Studio Code:** Development environment

## Data Source

Dataset: [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains historical retail transactions from December 2010 to December 2011.

**Original records:** 541,909

Key fields include invoice numbers, product codes, descriptions, quantities, transaction dates, unit prices, customer identifiers and countries.

The raw dataset is not included in this repository. It can be downloaded from the source above.

## ETL Pipeline Architecture

```text
Online Retail.xlsx
        |
        v
EXTRACT
Python + Pandas
        |
        v
TRANSFORM
Data Cleaning and Validation
        |
        +--> Standardised Transactions
        |
        +--> Positive Sales Records
        |
        v
LOAD
SQLAlchemy + pyodbc
        |
        v
SQL Server - RetailSalesETL
        |
        v
VALIDATE
Record Counts and Data Quality Checks
        |
        v
SQL Analytics and Business Insights
```

The entire pipeline is orchestrated through `main.py` and can be executed using a single command.

## ETL Implementation

### 1. Extract

The extraction script reads the original Excel dataset using Pandas.

It examines the source records, data types, missing values, duplicate rows, and potentially invalid transactions.

### 2. Transform

The transformation script standardises column names and data types, calculates transaction line values, and creates data quality indicators.

Key operations include:

- Standardising column names
- Converting transaction dates and numeric fields
- Identifying missing customer information
- Flagging duplicate records
- Identifying cancellations and nonpositive quantities
- Flagging nonpositive unit prices
- Calculating transaction line values
- Creating a positive-sales dataset

All source records are retained in the standardised transactions dataset.

### 3. Load

The load script transfers the transformed datasets into SQL Server.

Two destination tables are maintained:

| Table | Description |
|---|---|
| `retail_transactions` | All standardised records with data quality flags |
| `retail_sales` | Positive-quantity, positive-price sales excluding cancellation invoices |

The load uses a database transaction to refresh both tables together.

If an error occurs before committing the transaction, the database changes are rolled back.

### 4. Validate

Automated validation compares expected source record counts against the SQL Server tables and checks the consistency of positive-sales classifications.

The pipeline raises an error when a validation check fails.

## Data Quality Assessment

| Quality check | Result |
|---|---:|
| Original records | 541,909 |
| Missing customer IDs | 135,080 |
| Missing product descriptions | 1,454 |
| Duplicate rows flagged | 5,268 |
| Nonpositive quantities | 10,624 |
| Nonpositive unit prices | 2,517 |
| Cancellation invoice records | 9,288 |

Duplicate rows are retained but flagged for investigation. Missing customer identifiers do not automatically cause records to be excluded.

Returns, cancellations and nonpositive transaction values are preserved in the standardised dataset.

## ETL Validation Results

| Validation metric | Result |
|---|---:|
| Standardised records loaded | 541,909 |
| Positive-sales records loaded | 530,104 |
| Positive-sales classification count | 530,104 |
| Other transaction records | 11,805 |

All automated validation checks passed.

Repeated full-refresh executions produced consistent record counts without accumulating additional records.

## Business Analysis and Findings

### Overall Positive Sales Performance

| Metric | Result |
|---|---:|
| Positive sales value | 10,666,684.54 |
| Distinct invoices | 19,960 |
| Positive sales lines | 530,104 |
| Flagged duplicate sales lines | 5,226 |

### Top Three Countries by Positive Sales Value

| Country | Sales value |
|---|---:|
| United Kingdom | 9,025,222.08 |
| Netherlands | 285,446.34 |
| Ireland (EIRE) | 283,453.96 |

The United Kingdom accounted for the majority of positive sales value in the dataset.

### Highest-Performing Month

November 2011 recorded the highest positive sales value.

| Metric | Result |
|---|---:|
| Month | November 2011 |
| Positive sales value | 1,509,496.33 |
| Distinct invoices | 2,769 |
| Positive sales lines | 83,369 |

These results demonstrate how a processed dataset can support geographic and time-based business reporting.

## Project Structure

```text
Retail-Sales-ETL-Pipeline/
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- src/
|   |-- extract.py
|   |-- transform.py
|   |-- load.py
|   |-- validate.py
|   |-- config.py
|   |-- test_connection.py
|
|-- sql/
|   |-- 01_create_database.sql
|   |-- 02_create_tables.sql
|   |-- 03_sales_analytics.sql
|
|-- logs/
|
|-- main.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
```

## How to Run the Project

**Prerequisites:** Python, Microsoft SQL Server, a compatible Microsoft SQL Server ODBC driver, and access to the source dataset.

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure the SQL Server connection.
5. Download `Online Retail.xlsx` and place it inside `data/raw/`.
6. Execute `01_create_database.sql` and `02_create_tables.sql` in SQL Server Management Studio.
7. Run the complete pipeline:

   ```bash
   python main.py
   ```

8. Review the execution log in `logs/pipeline.log`.
9. Run `03_sales_analytics.sql` in SSMS to reproduce the business analysis.

The database connection uses Windows Authentication in the current implementation.

## Pipeline Reliability Features

- Automated execution of the ETL stages
- Data quality flags
- Transactional database refresh
- Record-count reconciliation
- Validation of sales classifications
- Pipeline execution logging
- Error handling and failure reporting
- Repeatable full-refresh execution
- Environment-based database configuration

## Limitations and Future Enhancements

- The dataset is historical and does not reflect current retail performance.
- Positive sales value excludes returns and cancellations and should not be described as net revenue.
- Flagged duplicate rows remain in the analytical dataset.
- The pipeline performs full refreshes rather than incremental loading.
- Record-count checks do not establish complete row-level data equivalence.
- The current implementation uses a local SQL Server instance.
- Future enhancements could include incremental loading, stronger row-level validation, automated tests, monitoring and Azure cloud integration.

## Project Outcome

The project successfully processed 541,909 retail transaction records, identified 530,104 positive-sales lines, loaded the transformed datasets into Microsoft SQL Server and passed automated validation checks.

It demonstrates an end-to-end ETL workflow, from raw data ingestion through reliable database loading to business-ready SQL analytics.