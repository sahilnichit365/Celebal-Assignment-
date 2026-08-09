SELECT
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
HAVING SUM(
    CASE
        WHEN o.status = 'DELIVERED' THEN 1
        ELSE 0
    END
) = 0
ORDER BY c.customer_id;


SELECT
    p.product_id,
    p.product_name,
    SUM(
        CASE
            WHEN oi.quantity > 0 THEN oi.quantity
            ELSE 0
        END
    ) AS purchased_quantity,
    SUM(
        CASE
            WHEN oi.quantity < 0 THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_quantity
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
HAVING returned_quantity > purchased_quantity
ORDER BY returned_quantity DESC;


SELECT
    p.category,
    SUM(
        CASE
            WHEN oi.quantity < 0 THEN ABS(oi.quantity)
            ELSE 0
        END
    ) AS returned_items,
    SUM(
        ABS(oi.quantity)
    ) AS total_items,
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN oi.quantity < 0 THEN ABS(oi.quantity)
                ELSE 0
            END
        )
        / NULLIF(SUM(ABS(oi.quantity)), 0),
        2
    ) AS return_rate_percent
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;