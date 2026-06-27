# SQL Assignment – E-Commerce Sales Database

# Overview

This project is part of the "Celebal Summer Internship 2026 – Week 2 SQL Assignment".

The objective of this assignment is to design a relational database, load sample data, and perform SQL operations including filtering, aggregation, joins, conditional logic, indexing, and transaction management using **SQL Server Management Studio (SSMS)**.

---

# Tools & Technologies

- SQL Server Management Studio (SSMS)
- Microsoft SQL Server
- SQL

# Database Name

Superstore


# Database Schema

The database consists of the following four tables:

1. **customers**
2. **products**
3. **orders**
4. **order_items**

Relationships:

- One Customer → Many Orders
- One Order → Many Order Items
- One Product → Many Order Items

# Project Structure

SQL_Assignment/
│
├── Database_Setup.sql
├── Insert_Data.sql
├── Section_A.sql
├── Section_B.sql
├── Section_C.sql
├── Section_D.sql
├── Section_E.sql
└── README.md


# Assignment Sections

# Database Setup

- Create Database
- Create Tables
- Create Indexes

# Data Loading

- Insert sample records into:
  - customers
  - products
  - orders
  - order_items

# Section A – SQL Basics

Covered:

- SELECT
- DISTINCT
- Primary Keys
- Constraints
- UNIQUE
- CHECK Constraints

# Section B – Filtering & Optimization

Covered:

- WHERE
- BETWEEN
- AND
- Date Filtering
- Indexes
- SARGable Queries


# Section C – Aggregation

Covered:

- COUNT()
- SUM()
- AVG()
- MAX()
- MIN()
- GROUP BY
- HAVING
- ORDER BY

---

# Section D – Joins & Relationships

Covered:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- FULL OUTER JOIN
- Foreign Keys
- Multi-table Joins

# Section E – Advanced SQL

Covered:

- CASE Statements
- Conditional Aggregation
- ACID Properties
- Transactions
- COMMIT
- ROLLBACK
- TRY...CATCH

# Sample Queries Performed

- Retrieve customer information
- Filter products by category and price
- Calculate total revenue
- Find average product price
- Monthly order analysis
- Customer and order joins
- Product-wise sales
- Order transaction processing
- Price categorization using CASE


# Learning Outcomes

After completing this assignment, I gained hands-on experience with:

- Database Design
- Table Creation
- Primary & Foreign Keys
- SQL Constraints
- Index Creation
- Data Insertion
- Data Retrieval
- Filtering Records
- Aggregate Functions
- SQL Joins
- CASE Expressions
- Transactions
- ACID Properties
- Query Optimization

# How to Run

1. Open **SQL Server Management Studio (SSMS)**.
2. Execute `Database_Setup.sql`.
3. Execute `Insert_Data.sql`.
4. Run each section file in order:
   - `Section_A.sql`
   - `Section_B.sql`
   - `Section_C.sql`
   - `Section_D.sql`
   - `Section_E.sql`
5. Verify the output of each query.


# Output

All queries were successfully executed in SQL Server Management Studio (SSMS), and the expected results were verified.


# Author

**Sahil Nichit**

B.E. Artificial Intelligence & Data Science

Dr. D. Y. Patil Institute of Technology, Pimpri, Pune
