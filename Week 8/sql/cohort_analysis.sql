WITH cohort_customers AS (
    SELECT
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),
customer_orders AS (
    SELECT DISTINCT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    WHERE o.customer_id IS NOT NULL
),
customer_activity AS (
    SELECT
        c.customer_id,
        c.cohort_month,
        o.order_month,
        (
            CAST(strftime('%Y', o.order_month || '-01') AS INTEGER) * 12
            + CAST(strftime('%m', o.order_month || '-01') AS INTEGER)
        )
        -
        (
            CAST(strftime('%Y', c.cohort_month || '-01') AS INTEGER) * 12
            + CAST(strftime('%m', c.cohort_month || '-01') AS INTEGER)
        ) AS month_number
    FROM cohort_customers c
    JOIN customer_orders o
        ON c.customer_id = o.customer_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(*) AS cohort_size
    FROM cohort_customers
    GROUP BY cohort_month
),
cohort_retention AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM customer_activity
    WHERE month_number BETWEEN 0 AND 3
    GROUP BY
        cohort_month,
        month_number
),
months AS (
    SELECT 0 AS month_number
    UNION ALL
    SELECT 1
    UNION ALL
    SELECT 2
    UNION ALL
    SELECT 3
)
SELECT
    cs.cohort_month,
    cs.cohort_size,
    m.month_number,
    COALESCE(cr.active_customers, 0) AS active_customers,
    ROUND(
        COALESCE(cr.active_customers, 0) * 100.0
        / NULLIF(cs.cohort_size, 0),
        2
    ) AS retention_rate
FROM cohort_sizes cs
CROSS JOIN months m
LEFT JOIN cohort_retention cr
    ON cs.cohort_month = cr.cohort_month
    AND m.month_number = cr.month_number
ORDER BY
    cs.cohort_month,
    m.month_number;