                --SECTION C – AGGREGATION--

-- Q13. Count the total number of orders

SELECT COUNT(*) AS Total_Orders
FROM orders;

-- Q14. Find total revenue from Delivered orders

SELECT SUM(total_amount) AS Total_Revenue
FROM orders
WHERE status = 'Delivered';

-- Q15. Calculate average unit price for each category

SELECT
    category,
    AVG(unit_price) AS Average_Unit_Price
FROM products
GROUP BY category;

-- Q16. Count of orders and total revenue by status

SELECT
    status,
    COUNT(order_id) AS Total_Orders,
    SUM(total_amount) AS Total_Revenue
FROM orders
GROUP BY status
ORDER BY Total_Revenue DESC;

-- Q17. Most expensive and cheapest product in each category

SELECT
    category,
    MAX(unit_price) AS Most_Expensive,
    MIN(unit_price) AS Cheapest
FROM products
GROUP BY category;

-- Q18. Categories where average unit price is greater than ₹2000

SELECT
    category,
    AVG(unit_price) AS Average_Unit_Price
FROM products
GROUP BY category
HAVING AVG(unit_price) > 2000;