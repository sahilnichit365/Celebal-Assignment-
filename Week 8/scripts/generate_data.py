import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 1000
NUM_ORDER_ITEMS = 2500


CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home",
    "Books"
]

SUBCATEGORIES = {
    "Electronics": [
        "Mobiles",
        "Laptops",
        "Headphones",
        "Accessories"
    ],
    "Clothing": [
        "Shirts",
        "Jeans",
        "Shoes",
        "Jackets"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor",
        "Lighting"
    ],
    "Books": [
        "Fiction",
        "Education",
        "Technology",
        "Biography"
    ]
}

ORDER_STATUSES = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

REGIONS = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]


def random_date(start_date, end_date):
    """Generate a random datetime between two dates."""

    time_difference = end_date - start_date

    random_seconds = random.randint(
        0,
        int(time_difference.total_seconds())
    )

    return start_date + timedelta(seconds=random_seconds)


def write_csv(filename, fieldnames, rows):
    """Write records to a CSV file."""

    filepath = RAW_DATA_DIR / filename

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {filepath}")


def generate_customers():
    customers = []

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)

    for customer_number in range(1, NUM_CUSTOMERS + 1):

        customer_id = f"CUST{customer_number:04d}"

        customer_name = fake.name()

        registration_date = random_date(
            start_date,
            end_date
        ).strftime("%Y-%m-%d")

        customer_type = random.choices(
            CUSTOMER_TYPES,
            weights=[70, 25, 5],
            k=1
        )[0]

        email = fake.email()

        if customer_number <= int(NUM_CUSTOMERS * 0.02):

            invalid_email_type = random.choice([
                "missing_at",
                "missing_domain"
            ])

            if invalid_email_type == "missing_at":
                email = email.replace("@", "")

            else:
                email = email.split("@")[0] + "@"

        customers.append({
            "customer_id": customer_id,
            "customer_name": customer_name,
            "email": email,
            "registration_date": registration_date,
            "customer_type": customer_type
        })

    return customers


def generate_products():
    products = []

    for product_number in range(1, NUM_PRODUCTS + 1):

        product_id = f"PROD{product_number:04d}"

        category = random.choice(CATEGORIES)

        subcategory = random.choice(
            SUBCATEGORIES[category]
        )

        product_name = (
            f"{subcategory} "
            f"{fake.word().capitalize()}"
        )

        if product_number % 10 == 0:
            product_name = f"  {product_name.upper()}  "

        elif product_number % 7 == 0:
            product_name = f" {product_name.lower()} "

        cost_price = round(
            random.uniform(50, 50000),
            2
        )

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price
        })

    return products

def generate_orders(customers):
    orders = []

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)

    customer_ids = [
        customer["customer_id"]
        for customer in customers
    ]

    missing_customer_count = int(
        NUM_ORDERS * 0.05
    )

    for order_number in range(1, NUM_ORDERS + 1):

        order_id = f"ORD{order_number:05d}"

        customer_id = random.choice(customer_ids)

        if order_number <= missing_customer_count:
            customer_id = ""

        order_datetime = random_date(
            start_date,
            end_date
        )

        if order_number % 20 == 0:

            order_date = order_datetime.strftime(
                "%d-%m-%Y"
            )

        else:

            order_date = order_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        status = random.choice(ORDER_STATUSES)

        region_code = random.choice(REGIONS)

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status,
            "region_code": region_code
        })

    return orders


def generate_order_items(orders, products):
    order_items = []

    valid_order_ids = [
        order["order_id"]
        for order in orders
    ]

    product_ids = [
        product["product_id"]
        for product in products
    ]

    negative_quantity_count = int(
        NUM_ORDER_ITEMS * 0.03
    )

    for item_number in range(1, NUM_ORDER_ITEMS + 1):

        item_id = f"ITEM{item_number:06d}"

        order_id = random.choice(
            valid_order_ids
        )

        product_id = random.choice(
            product_ids
        )

        quantity = random.randint(1, 10)

        if item_number <= negative_quantity_count:
            quantity = -random.randint(1, 5)

        unit_price = round(
            random.uniform(100, 50000),
            2
        )

        discount_percent = round(
            random.uniform(0, 100),
            2
        )

        order_items.append({
            "item_id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent
        })

    return order_items


def main():

    print("\nStarting e-commerce dataset generation...\n")

    customers = generate_customers()

    products = generate_products()

    orders = generate_orders(
        customers
    )

    order_items = generate_order_items(
        orders,
        products
    )

    write_csv(
        "customers.csv",
        [
            "customer_id",
            "customer_name",
            "email",
            "registration_date",
            "customer_type"
        ],
        customers
    )

    write_csv(
        "products.csv",
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "cost_price"
        ],
        products
    )

    # Write orders.csv
    write_csv(
        "orders.csv",
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "region_code"
        ],
        orders
    )

    # Write order_items.csv
    write_csv(
        "order_items.csv",
        [
            "item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_percent"
        ],
        order_items
    )

    print("\nDataset generation completed successfully!")

    print("\nRows generated:")
    print(f"Customers    : {len(customers)}")
    print(f"Products     : {len(products)}")
    print(f"Orders       : {len(orders)}")
    print(f"Order Items  : {len(order_items)}")

    print(
        f"\nFiles saved inside:\n{RAW_DATA_DIR}"
    )


if __name__ == "__main__":
    main()