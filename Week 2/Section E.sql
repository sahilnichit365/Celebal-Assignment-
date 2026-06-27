                --SECTION E – ADVANCED CONCEPTS--

-- Q24. Classify products into price tiers using CASE

SELECT
    product_name,
    unit_price,
    CASE
        WHEN unit_price < 1000 THEN 'Budget'
        WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
        WHEN unit_price > 3000 THEN 'Premium'
    END AS price_tier
FROM products;


-- Q25. Count Delivered vs Not Delivered orders

SELECT
    SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS Delivered_Orders,
    SUM(CASE WHEN status <> 'Delivered' THEN 1 ELSE 0 END) AS Not_Delivered_Orders
FROM orders;


-- Q26. ACID Properties

/*

ACID Properties

A - Atomicity
--------------
Ensures that a transaction is completed entirely or not at all.
If one step fails, all previous steps are rolled back.

Example:
If money is deducted from Account A but not added to Account B,
the transaction is rolled back.

-------------------------------------------------------

C - Consistency
---------------
Ensures that the database remains valid before and after
every transaction.

Example:
Bank balance should never become negative due to an invalid transaction.

-------------------------------------------------------

I - Isolation
-------------
Ensures multiple users can perform transactions simultaneously
without affecting each other.

Example:
Two people withdrawing money from the same account
at the same time should not produce incorrect balances.

-------------------------------------------------------

D - Durability
--------------
Once a transaction is committed,
the data remains permanently stored,
even if the server crashes.

Example:
After transferring money successfully,
the transaction remains saved even after power failure.

*/


-- Q27. Transaction Example

BEGIN TRANSACTION;

BEGIN TRY

    -- Insert new order

    INSERT INTO orders
    (
        order_id,
        customer_id,
        order_date,
        status,
        total_amount
    )
    VALUES
    (
        1011,
        102,
        GETDATE(),
        'Pending',
        1598.00
    );


    -- Insert Order Item 1

    INSERT INTO order_items
    (
        item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_pct
    )
    VALUES
    (
        5016,
        1011,
        206,
        1,
        1299.00,
        0
    );


    -- Insert Order Item 2

    INSERT INTO order_items
    (
        item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        discount_pct
    )
    VALUES
    (
        5017,
        1011,
        208,
        1,
        299.00,
        0
    );


    -- Update Stock

    UPDATE products
    SET stock_qty = stock_qty - 1
    WHERE product_id = 206;

    UPDATE products
    SET stock_qty = stock_qty - 1
    WHERE product_id = 208;


    COMMIT TRANSACTION;

    PRINT 'Transaction Committed Successfully';

END TRY

BEGIN CATCH

    ROLLBACK TRANSACTION;

    PRINT 'Transaction Failed';

    PRINT ERROR_MESSAGE();

END CATCH;