
-- Create database for the Retail Sales ETL Pipeline

IF DB_ID('RetailSalesETL') IS NULL
BEGIN
    CREATE DATABASE RetailSalesETL;
END;
GO

USE RetailSalesETL;
GO

SELECT DB_NAME() AS CurrentDatabase;
