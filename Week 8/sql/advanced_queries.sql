WITH daily_revenue AS (
    SELECT
        o.region_code,
        date(o.order_date) AS order_date,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS daily_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.region_code,
        date(o.order_date)
)
SELECT
    region_code,
    order_date,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(
        SUM(daily_revenue) OVER (
            PARTITION BY region_code
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_total
FROM daily_revenue
ORDER BY
    region_code,
    order_date;


WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS total_revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY
        p.category,
        p.product_id,
        p.product_name
)
SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS rank_in_category
FROM product_revenue
ORDER BY
    category,
    rank_in_category,
    product_name;


WITH customer_orders AS (
    SELECT
        o.customer_id,
        datetime(o.order_date) AS order_date
    FROM orders o
    WHERE o.customer_id IS NOT NULL
),
order_gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_order_date
    FROM customer_orders
),
gap_values AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,
        CASE
            WHEN previous_order_date IS NOT NULL
            THEN ROUND(
                julianday(order_date) -
                julianday(previous_order_date),
                2
            )
        END AS days_gap
    FROM order_gaps
),
customer_risk AS (
    SELECT
        customer_id,
        AVG(days_gap) AS average_gap
    FROM gap_values
    GROUP BY customer_id
)
SELECT
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    CASE
        WHEN r.average_gap > 30 THEN 'At Risk'
        ELSE 'Not At Risk'
    END AS risk_status
FROM gap_values g
JOIN customer_risk r
    ON g.customer_id = r.customer_id
ORDER BY
    g.customer_id,
    g.order_date;


WITH monthly_customer_revenue AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS revenue_month,
        o.customer_id,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.customer_id IS NOT NULL
    GROUP BY
        strftime('%Y-%m', o.order_date),
        o.customer_id
),
customer_categories AS (
    SELECT
        revenue_month,
        customer_id,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue >= 5000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_category
    FROM monthly_customer_revenue
)
SELECT
    revenue_month,
    revenue_category,
    COUNT(*) AS customer_count
FROM customer_categories
GROUP BY
    revenue_month,
    revenue_category
ORDER BY
    revenue_month,
    CASE revenue_category
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;


WITH customer_lifetime_value AS (
    SELECT
        c.customer_id,
        COALESCE(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),
            0
        ) AS total_value
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id
),
quartiles AS (
    SELECT
        customer_id,
        total_value,
        NTILE(4) OVER (
            ORDER BY total_value DESC
        ) AS quartile
    FROM customer_lifetime_value
)
SELECT
    customer_id,
    ROUND(total_value, 2) AS total_value,
    quartile,
    CASE quartile
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        WHEN 4 THEN 'Bronze'
    END AS quartile_label
FROM quartiles
ORDER BY quartile, total_value DESC;


WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        year,
        month
)
SELECT
    current.year,
    current.month,
    ROUND(current.revenue, 2) AS revenue,
    ROUND(previous.revenue, 2) AS prev_year_revenue,
    CASE
        WHEN previous.revenue IS NULL THEN NULL
        WHEN previous.revenue = 0 THEN NULL
        ELSE ROUND(
            (
                (current.revenue - previous.revenue)
                / previous.revenue
            ) * 100,
            2
        )
    END AS yoy_growth_percent
FROM monthly_revenue current
LEFT JOIN monthly_revenue previous
    ON previous.year = current.year - 1
    AND previous.month = current.month
ORDER BY
    current.year,
    current.month;


WITH customer_categories AS (
    SELECT
        o.customer_id,
        p.category,
        datetime(o.order_date) AS order_date
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.customer_id IS NOT NULL
),
category_values AS (
    SELECT
        customer_id,
        FIRST_VALUE(category) OVER (
            PARTITION BY customer_id
            ORDER BY order_date ASC
        ) AS first_category,
        FIRST_VALUE(category) OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC
        ) AS latest_category
    FROM customer_categories
)
SELECT DISTINCT
    customer_id,
    first_category,
    latest_category,
    CASE
        WHEN first_category <> latest_category THEN 'Yes'
        ELSE 'No'
    END AS category_shift
FROM category_values
ORDER BY customer_id;


WITH customer_revenue AS (
    SELECT
        c.customer_id,
        COALESCE(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ),
            0
        ) AS revenue
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id
),
cumulative AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue,
        SUM(revenue) OVER () AS total_revenue
    FROM customer_revenue
)
SELECT
    customer_id,
    ROUND(revenue, 2) AS revenue,
    ROUND(cumulative_revenue, 2) AS cumulative_revenue,
    ROUND(
        CASE
            WHEN total_revenue = 0 THEN 0
            ELSE cumulative_revenue * 100.0 / total_revenue
        END,
        2
    ) AS cumulative_percent
FROM cumulative
ORDER BY revenue DESC;


WITH order_pairs AS (
    SELECT
        oi1.product_id AS product_a,
        oi2.product_id AS product_b,
        oi1.order_id
    FROM order_items oi1
    JOIN order_items oi2
        ON oi1.order_id = oi2.order_id
        AND oi1.product_id < oi2.product_id
),
pair_counts AS (
    SELECT
        product_a,
        product_b,
        COUNT(DISTINCT order_id) AS times_bought_together
    FROM order_pairs
    GROUP BY
        product_a,
        product_b
)
SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    times_bought_together
FROM pair_counts pc
JOIN products p1
    ON pc.product_a = p1.product_id
JOIN products p2
    ON pc.product_b = p2.product_id
ORDER BY
    times_bought_together DESC,
    product_a,
    product_b;