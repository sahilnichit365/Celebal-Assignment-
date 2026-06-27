               --SECTION B – FILTERING & OPTIMIZATION--

-- Q7. Retrieve all orders with status = 'Delivered'

SELECT *
FROM orders
WHERE status = 'Delivered';

-- Q8. Find all Electronics products with unit_price > 2000

SELECT *
FROM products
WHERE category = 'Electronics'
AND unit_price > 2000;

-- Q9. Customers who joined in 2024 and belong to Maharashtra

SELECT *
FROM customers
WHERE join_date >= '2024-01-01'
AND join_date < '2025-01-01'
AND state = 'Maharashtra';

-- Q10. Orders placed between
-- '2024-08-10' and '2024-08-25'
-- excluding Cancelled orders

SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
AND status <> 'Cancelled';

-- Q11. Query using index on order_date

SELECT *
FROM orders
WHERE order_date >= '2024-08-01'
AND order_date <= '2024-08-31';

-- Q12. SARGable Query

SELECT *
FROM customers
WHERE join_date >= '2024-01-01'
AND join_date < '2025-01-01';

