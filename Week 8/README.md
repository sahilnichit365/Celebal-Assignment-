# E-Commerce Order Analytics System

## Project Overview

The E-Commerce Order Analytics System is an end-to-end data analytics project developed using Python, Pandas, and SQLite.

The system generates realistic e-commerce datasets with intentional data-quality issues, cleans and validates the data, loads the cleaned data into SQLite, performs business analysis using SQL, and provides a Python command-line reporting tool.

## Objectives

- Generate realistic e-commerce datasets using Python.
- Introduce intentional data inconsistencies.
- Clean and validate data using Pandas.
- Check referential integrity across tables.
- Store cleaned data in SQLite.
- Perform basic, intermediate, and advanced SQL analysis.
- Use joins, aggregations, window functions, CTEs, and cohort analysis.
- Build a Python command-line reporting tool.
- Handle important edge cases.
- Generate business insights from e-commerce order data.

## Technologies Used

- Python
- Pandas
- Faker
- SQLite
- SQL
- Python sqlite3

## Project Structure

```text
ecommerce-analytics-system/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   │
│   └── cleaned/
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── orders_clean.csv
│       ├── order_items_clean.csv
│       └── data_quality_report.txt
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── run_sql.py
│   └── report_cli.py
│
├── sql/
│   ├── schema.sql
│   ├── basic_queries.sql
│   ├── intermediate_queries.sql
│   ├── advanced_queries.sql
│   └── cohort_analysis.sql
│
├── tests/
│   └── test_edge_cases.py
│
├── output/
│   └── sample_reports/
│
├── ecommerce.db
└── README.md