import sqlite3
from datetime import datetime, timedelta


def test_invalid_order_reference():
    connection = sqlite3.connect(":memory:")

    connection.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY
        )
    """)

    connection.execute("""
        CREATE TABLE order_items (
            item_id TEXT PRIMARY KEY,
            order_id TEXT,
            FOREIGN KEY (order_id)
            REFERENCES orders(order_id)
        )
    """)

    connection.execute(
        "INSERT INTO orders VALUES (?)",
        ("ORD001",)
    )

    connection.execute(
        "INSERT INTO order_items VALUES (?, ?)",
        ("ITEM001", "INVALID_ORDER")
    )

    result = connection.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
        ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
    """).fetchone()[0]

    assert result == 1

    connection.close()

    print("Test 1 passed: Invalid order reference detected")


def test_discount_greater_than_100():
    discount = 120

    is_invalid = (
        discount < 0
        or discount > 100
    )

    assert is_invalid is True

    print("Test 2 passed: Discount greater than 100 detected")


def test_zero_quantity():
    quantity = 0

    is_zero_quantity = (
        quantity == 0
    )

    assert is_zero_quantity is True

    print("Test 3 passed: Zero quantity detected")


def test_future_order_date():
    today = datetime.now().date()

    future_date = (
        today + timedelta(days=30)
    )

    is_future_date = (
        future_date > today
    )

    assert is_future_date is True

    print("Test 4 passed: Future order date detected")


def run_tests():
    test_invalid_order_reference()
    test_discount_greater_than_100()
    test_zero_quantity()
    test_future_order_date()

    print()
    print("All edge case tests passed successfully!")


if __name__ == "__main__":
    run_tests()