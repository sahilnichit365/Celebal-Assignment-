                --SECTION D – JOINS & RELATIONSHIPS--

-- Q19. INNER JOIN
-- Display order details along with customer name


SELECT
    o.order_id,
    o.order_date,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id;

-- Q20. LEFT JOIN
-- Display all customers and their orders

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id;

-- Q21. JOIN Three Tables
-- Display order items with product details

SELECT
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON oi.product_id = p.product_id
ORDER BY o.order_id;

-- Q22. Difference between LEFT JOIN and RIGHT JOIN

/*
LEFT JOIN:
Returns ALL rows from the LEFT table
(customers) and matching rows from orders.
If there is no matching order,
NULL values are returned.

Example:
*/

SELECT
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;


/*
RIGHT JOIN:
Returns ALL rows from the RIGHT table
(orders) and matching rows from customers.

Example:
*/

SELECT
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id;


/*
FULL OUTER JOIN:

Returns all rows from both tables.
If there is no match,
NULL values are returned.

Use when you want every customer
and every order,
including unmatched records.
*/

-----------------------------------------------------------
-- Q23. Foreign Key Relationships
-----------------------------------------------------------

/*
Foreign Keys:

orders.customer_id
    → customers.customer_id

order_items.order_id
    → orders.order_id

order_items.product_id
    → products.product_id


If we try to insert:

customer_id = 999

into the orders table,

SQL Server will generate a

FOREIGN KEY constraint error

because customer_id 999
does not exist in customers table.
*/

-- Example

INSERT INTO orders
VALUES
(
1011,
999,
'2024-09-01',
'Pending',
2000.00
);

-- Expected Error:
-- The INSERT statement conflicted with the FOREIGN KEY constraint.