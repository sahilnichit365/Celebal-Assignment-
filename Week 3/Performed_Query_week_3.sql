-- 1)Find all orders where sales are greater than the average sales. 

SELECT
    order_id,
    customer_id,
    sales
FROM orders
WHERE sales >
(
    SELECT AVG(sales)
    FROM orders
)
ORDER BY sales DESC;



-- 2)Find the highest sales order for each customer Using Correlated Subquery

SELECT
    o.customer_id,
    c.customer_name,
    o.order_id,
    o.sales
FROM orders o JOIN customers c
ON o.customer_id = c.customer_id
WHERE o.sales =
(
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
)
ORDER BY c.customer_name;



-- 3)Calculate Total Sales for Each Customer Using CTE

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
ORDER BY cs.total_sales DESC;



-- 4)Find customers whose total sales are above the average customer sales
-- Using CTE and Subquery

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT DISTINCT
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



-- 5)Rank all customers based on total sales using Window Function  

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT DISTINCT
    c.customer_name,
    cs.total_sales,

    RANK() OVER
    (
        ORDER BY cs.total_sales DESC
    ) AS customer_rank

FROM CustomerSales cs JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY customer_rank;



-- 6)Find the highest value order for each customer Using ROW_NUMBER()

WITH OrderRanking AS
(
    SELECT
        customer_id,
        order_id,
        sales,

        ROW_NUMBER() OVER
        (
            PARTITION BY customer_id
            ORDER BY sales DESC
        ) AS row_num

    FROM orders
)
SELECT
    c.customer_name,
    o.order_id,
    o.sales
FROM OrderRanking o JOIN customers c
ON o.customer_id = c.customer_id
WHERE row_num = 1
ORDER BY o.sales DESC;



-- 7)Display top 3 customers based on total sales. (Window Function)  

WITH CustomerSales AS
(
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
),
CustomerRanking AS
(
    SELECT
        customer_id,
        total_sales,

        RANK() OVER
        (
            ORDER BY total_sales DESC
        ) AS customer_rank

    FROM CustomerSales
)
SELECT
    c.customer_name,
    cr.total_sales,
    cr.customer_rank
FROM CustomerRanking cr JOIN customers c
ON cr.customer_id = c.customer_id
WHERE customer_rank <= 3
ORDER BY customer_rank;


