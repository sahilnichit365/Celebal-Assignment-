import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "ecommerce.db"


def parse_date(value):
    try:
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Date must be in YYYY-MM-DD format."
        )


def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError(
            "Start date cannot be after end date."
        )


def get_connection():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            "Database file ecommerce.db was not found."
        )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def get_period_summary(
    connection,
    start_date,
    end_date
):
    query = """
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            COALESCE(
                SUM(
                    oi.quantity *
                    oi.unit_price *
                    (1 - oi.discount_percent / 100.0)
                ),
                0
            ) AS revenue,
            COUNT(
                DISTINCT o.customer_id
            ) AS unique_customers
        FROM orders o
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE date(o.order_date)
              BETWEEN ? AND ?
    """

    cursor = connection.execute(
        query,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    return cursor.fetchone()


def get_top_products(
    connection,
    start_date,
    end_date
):
    query = """
        SELECT
            p.product_name,
            SUM(oi.quantity) AS quantity_sold,
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            ) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE date(o.order_date)
              BETWEEN ? AND ?
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY revenue DESC
        LIMIT 3
    """

    cursor = connection.execute(
        query,
        (
            start_date.isoformat(),
            end_date.isoformat()
        )
    )

    return cursor.fetchall()


def get_previous_period(
    start_date,
    end_date
):
    period_length = (
        end_date - start_date
    ).days + 1

    previous_end = (
        start_date - timedelta(days=1)
    )

    previous_start = (
        previous_end
        - timedelta(days=period_length - 1)
    )

    return previous_start, previous_end


def calculate_change(
    current_value,
    previous_value
):
    if previous_value is None:
        return None

    if previous_value == 0:
        return None

    return (
        (current_value - previous_value)
        / previous_value
    ) * 100


def print_line():
    print("-" * 70)


def print_summary(
    report_type,
    start_date,
    end_date,
    current,
    previous,
    previous_start,
    previous_end,
    top_products
):
    print()
    print("=" * 70)
    print("E-COMMERCE ORDER ANALYTICS REPORT")
    print("=" * 70)

    print(f"Report Type : {report_type}")
    print(
        f"Date Range  : "
        f"{start_date} to {end_date}"
    )

    print()
    print("SUMMARY")
    print_line()

    total_orders = current["total_orders"]
    revenue = current["revenue"] or 0
    unique_customers = current["unique_customers"]

    previous_orders = (
        previous["total_orders"] or 0
    )

    previous_revenue = (
        previous["revenue"] or 0
    )

    previous_customers = (
        previous["unique_customers"] or 0
    )

    order_change = calculate_change(
        total_orders,
        previous_orders
    )

    revenue_change = calculate_change(
        revenue,
        previous_revenue
    )

    customer_change = calculate_change(
        unique_customers,
        previous_customers
    )

    print(
        f"Total Orders       : {total_orders}"
    )

    print(
        f"Revenue            : ₹{revenue:,.2f}"
    )

    print(
        f"Unique Customers   : {unique_customers}"
    )

    print()
    print("PREVIOUS PERIOD")
    print_line()

    print(
        f"Date Range         : "
        f"{previous_start} to {previous_end}"
    )

    print(
        f"Orders             : {previous_orders}"
    )

    print(
        f"Revenue            : "
        f"₹{previous_revenue:,.2f}"
    )

    print(
        f"Unique Customers   : "
        f"{previous_customers}"
    )

    print()
    print("PERCENTAGE CHANGE")
    print_line()

    print(
        f"Orders             : "
        f"{format_change(order_change)}"
    )

    print(
        f"Revenue            : "
        f"{format_change(revenue_change)}"
    )

    print(
        f"Unique Customers   : "
        f"{format_change(customer_change)}"
    )

    print()
    print("TOP 3 PRODUCTS")
    print_line()

    if not top_products:
        print("No products found for this date range.")

    else:
        print(
            f"{'Product':35} "
            f"{'Qty':>10} "
            f"{'Revenue':>18}"
        )

        print_line()

        for product in top_products:

            product_name = (
                product["product_name"][:35]
            )

            quantity = (
                product["quantity_sold"]
            )

            product_revenue = (
                product["revenue"] or 0
            )

            print(
                f"{product_name:35} "
                f"{quantity:>10} "
                f"₹{product_revenue:>16,.2f}"
            )

    print()
    print("=" * 70)


def format_change(value):
    if value is None:
        return "N/A"

    return f"{value:+.2f}%"


def main():

    parser = argparse.ArgumentParser(
        description="E-Commerce Order Analytics CLI"
    )

    parser.add_argument(
        "--report",
        required=True,
        choices=[
            "daily",
            "weekly",
            "monthly"
        ]
    )

    parser.add_argument(
        "--start-date",
        required=True,
        type=parse_date
    )

    parser.add_argument(
        "--end-date",
        required=True,
        type=parse_date
    )

    args = parser.parse_args()

    try:

        validate_date_range(
            args.start_date,
            args.end_date
        )

        connection = get_connection()

        current = get_period_summary(
            connection,
            args.start_date,
            args.end_date
        )

        previous_start, previous_end = (
            get_previous_period(
                args.start_date,
                args.end_date
            )
        )

        previous = get_period_summary(
            connection,
            previous_start,
            previous_end
        )

        top_products = get_top_products(
            connection,
            args.start_date,
            args.end_date
        )

        print_summary(
            args.report,
            args.start_date,
            args.end_date,
            current,
            previous,
            previous_start,
            previous_end,
            top_products
        )

        connection.close()

    except FileNotFoundError as error:
        print(f"Error: {error}")

    except ValueError as error:
        print(f"Error: {error}")

    except sqlite3.Error as error:
        print(
            f"Database error: {error}"
        )


if __name__ == "__main__":
    main()