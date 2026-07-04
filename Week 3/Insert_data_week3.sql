INSERT INTO customers
SELECT DISTINCT
    Customer_ID,
    Customer_Name,
    Segment,
    Country,
    City,
    State,
    Postal_Code,
    Region
FROM superstore_raw;



INSERT INTO products
SELECT DISTINCT
    Product_ID,
    Category,
    Sub_Category,
    Product_Name
FROM superstore_raw;



INSERT INTO orders
SELECT
    Order_ID,
    Order_Date,
    Ship_Date,
    Ship_Mode,
    Customer_ID,
    Product_ID,
    Sales,
    Quantity,
    Discount,
    Profit
FROM superstore_raw;



SELECT COUNT(*) 
FROM customers;

SELECT COUNT(*) 
FROM products;

SELECT COUNT(*) 
FROM orders;