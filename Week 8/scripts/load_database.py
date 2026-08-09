import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

CLEAN_DIR = BASE_DIR / "data" / "cleaned"
SQL_DIR = BASE_DIR / "sql"

DATABASE_PATH = BASE_DIR / "ecommerce.db"
SCHEMA_PATH = SQL_DIR / "schema.sql"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        schema = file.read()
    connection.executescript(schema)

    return connection


def load_table(connection, filename, table_name):
    filepath = CLEAN_DIR / filename

    df = pd.read_csv(filepath)

    df.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False
    )

    print(
        f"{table_name}: {len(df)} rows loaded"
    )


def verify_counts(connection):
    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    print("\nDatabase row counts:")

    for table in tables:

        cursor = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table}: {count}"
        )


def verify_relationships(connection):
    print("\nRelationship checks:")

    cursor = connection.execute(
        """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN orders o
        ON oi.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    )

    invalid_orders = cursor.fetchone()[0]

    print(
        f"Invalid order references: {invalid_orders}"
    )

    cursor = connection.execute(
        """
        SELECT COUNT(*)
        FROM order_items oi
        LEFT JOIN products p
        ON oi.product_id = p.product_id
        WHERE p.product_id IS NULL
        """
    )

    invalid_products = cursor.fetchone()[0]

    print(
        f"Invalid product references: {invalid_products}"
    )


def main():
    print("\nCreating SQLite database...\n")

    connection = create_database()

    load_table(
        connection,
        "customers_clean.csv",
        "customers"
    )

    load_table(
        connection,
        "products_clean.csv",
        "products"
    )

    load_table(
        connection,
        "orders_clean.csv",
        "orders"
    )

    load_table(
        connection,
        "order_items_clean.csv",
        "order_items"
    )

    connection.commit()

    verify_counts(connection)
    verify_relationships(connection)

    connection.close()

    print(
        "\nSQLite database created successfully!"
    )


if __name__ == "__main__":
    main()