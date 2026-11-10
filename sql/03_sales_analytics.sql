
USE RetailSalesETL;
GO

-- ============================================================
-- RETAIL SALES ETL - BUSINESS ANALYTICS
-- ============================================================
-- Objective:
-- Demonstrate how the processed retail transactions
-- support business reporting and decision-making.
--
-- Note:
-- Sales values represent positive transaction lines.
-- Returns are excluded and flagged duplicates are retained.
-- ============================================================


-- ============================================================
-- 1. OVERALL SALES PERFORMANCE
-- ============================================================
-- Business question:
-- How many sales transactions were recorded, and what
-- is the total value of positive sales?

SELECT
    COUNT_BIG(*) AS TotalSalesLines,
    COUNT(DISTINCT invoice_no) AS TotalInvoices,
    SUM(line_total) AS TotalSalesValue,
    SUM(
        CASE WHEN is_duplicate = 1 THEN 1 ELSE 0 END
    ) AS FlaggedDuplicateLines

FROM dbo.retail_sales;


-- ============================================================
-- 2. TOP 10 COUNTRIES BY SALES VALUE
-- ============================================================
-- Business question:
-- Which countries generated the highest positive sales?

SELECT TOP (10)
    country,
    COUNT_BIG(*) AS TotalSalesLines,
    COUNT(DISTINCT invoice_no) AS TotalInvoices,
    ROUND(SUM(line_total), 2) AS TotalSalesValue

FROM dbo.retail_sales

GROUP BY country

ORDER BY TotalSalesValue DESC;


-- ============================================================
-- 3. MONTHLY SALES TRENDS
-- ============================================================
-- Business question:
-- How did positive sales change over time?

SELECT
    CONVERT(CHAR(7), invoice_date, 120) AS SalesMonth,
    COUNT(DISTINCT invoice_no) AS TotalInvoices,
    COUNT_BIG(*) AS TotalSalesLines,
    ROUND(SUM(line_total), 2) AS TotalSalesValue

FROM dbo.retail_sales

WHERE invoice_date IS NOT NULL

GROUP BY CONVERT(CHAR(7), invoice_date, 120)

ORDER BY SalesMonth;


-- ============================================================
-- 4. HIGHEST SALES MONTH
-- ============================================================
-- Identify the month with the highest positive sales value.

SELECT TOP (1)
    CONVERT(CHAR(7), invoice_date, 120) AS SalesMonth,
    COUNT(DISTINCT invoice_no) AS TotalInvoices,
    COUNT_BIG(*) AS TotalSalesLines,
    ROUND(SUM(line_total), 2) AS TotalSalesValue

FROM dbo.retail_sales

WHERE invoice_date IS NOT NULL

GROUP BY CONVERT(CHAR(7), invoice_date, 120)

ORDER BY TotalSalesValue DESC;
