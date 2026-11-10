
USE RetailSalesETL;
GO

-- ============================================================
-- RETAIL SALES ETL: DATABASE TABLE SETUP
-- ============================================================
-- Purpose:
-- Create the destination tables for the Python ETL pipeline.
-- Existing tables are preserved when this script is rerun.


-- 1. Create the standardised transactions table

IF OBJECT_ID('dbo.retail_transactions', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.retail_transactions
    (
        invoice_no NVARCHAR(30) NULL,
        stock_code NVARCHAR(50) NULL,
        description NVARCHAR(500) NULL,
        quantity INT NULL,
        invoice_date DATETIME NULL,
        unit_price DECIMAL(18,4) NULL,
        customer_id INT NULL,
        country NVARCHAR(100) NULL,
        is_duplicate BIT NULL,
        is_cancellation BIT NULL,
        is_nonpositive_quantity BIT NULL,
        is_nonpositive_price BIT NULL,
        line_total DECIMAL(18,4) NULL,
        is_valid_sale BIT NULL
    );
END;
GO


-- 2. Create the positive-sales table

IF OBJECT_ID('dbo.retail_sales', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.retail_sales
    (
        invoice_no NVARCHAR(30) NULL,
        stock_code NVARCHAR(50) NULL,
        description NVARCHAR(500) NULL,
        quantity INT NULL,
        invoice_date DATETIME NULL,
        unit_price DECIMAL(18,4) NULL,
        customer_id INT NULL,
        country NVARCHAR(100) NULL,
        is_duplicate BIT NULL,
        is_cancellation BIT NULL,
        is_nonpositive_quantity BIT NULL,
        is_nonpositive_price BIT NULL,
        line_total DECIMAL(18,4) NULL,
        is_valid_sale BIT NULL
    );
END;
GO


-- 3. Verify that both tables exist

SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN (
      'retail_transactions',
      'retail_sales'
  )
ORDER BY TABLE_NAME;
