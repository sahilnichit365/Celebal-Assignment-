-- 1)Who are the top 5 customers?  

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT TOP 5
    c.customer_name,
    cs.total_sales
FROM CustomerSales cs JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY cs.total_sales DESC;



-- 2)Who are the bottom 5 customers?  

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT TOP 5
    c.customer_name,
    cs.total_sales
FROM CustomerSales cs
JOIN customers c
    ON cs.customer_id = c.customer_id
ORDER BY cs.total_sales ASC;



-- 3)Which customers made only one order?  

SELECT
    c.customer_name,
    COUNT(o.order_id) AS total_orders
FROM customers c JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING COUNT(o.order_id) = 1;



-- 4)Which customers have above-average sales?

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    cs.total_sales
FROM CustomerSales cs JOIN customers c
ON cs.customer_id = c.customer_id
WHERE cs.total_sales >
(
    SELECT AVG(total_sales)
    FROM CustomerSales
)
ORDER BY cs.total_sales DESC;



-- 5)What is the highest order value per customer? 

SELECT
    c.customer_name,
    MAX(o.sales) AS highest_order_value
FROM customers c JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY
    c.customer_name
ORDER BY
    highest_order_value DESC;
