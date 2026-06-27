                --SECTION A – SQL BASICS--

-- Q1. Display all columns and rows from customers table

SELECT *
FROM customers;


-- Q2. Display first name, last name and city

SELECT
    first_name,
    last_name,
    city
FROM customers;


-- Q3. Display all unique product categories

SELECT DISTINCT category
FROM products;


-- Q4. Primary Keys of all tables

/*
customers      -> customer_id
products       -> product_id
orders         -> order_id
order_items    -> item_id

Primary Key:
1. Must be UNIQUE.
2. Cannot contain NULL values.
3. Identifies each record uniquely.
*/

-- Q5. Constraints on email column

/*
The email column has:

1. UNIQUE Constraint
2. NOT NULL Constraint

Trying to insert a duplicate email will produce an error.

Example:
*/

INSERT INTO customers
VALUES
(
109,
'Rahul',
'Patil',
'aarav.s@email.com',
'Pune',
'Maharashtra',
'2024-09-01',
1
);

-- Expected Error:
-- Violation of UNIQUE KEY constraint.


-- Q6. CHECK Constraint Example

INSERT INTO products
VALUES
(
209,
'Keyboard',
'Electronics',
'HP',
-50,
100
);

-- Expected Error:
-- The CHECK constraint "unit_price > 0" prevents negative prices.
