USE SuperStoreDB;
GO

CREATE TABLE customers
(
    customer_id NVARCHAR(20),
    customer_name NVARCHAR(100),
    segment NVARCHAR(50),
    country NVARCHAR(50),
    city NVARCHAR(50),
    state NVARCHAR(50),
    postal_code INT,
    region NVARCHAR(30)
);
GO



CREATE TABLE products
(
    product_id NVARCHAR(30),
    category NVARCHAR(50),
    sub_category NVARCHAR(50),
    product_name NVARCHAR(200)
);
GO



CREATE TABLE orders
(
    order_id NVARCHAR(30),
    order_date DATE,
    ship_date DATE,
    ship_mode NVARCHAR(50),
    customer_id NVARCHAR(20),
    product_id NVARCHAR(30),
    sales DECIMAL(10,2),
    quantity INT,
    discount DECIMAL(5,2),
    profit DECIMAL(10,2)
);
GO