import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

ISSUE_REPORT = CLEAN_DIR / "data_quality_report.txt"

issues = []


def add_issue(issue_type, description, count):
    issues.append({
        "issue_type": issue_type,
        "description": description,
        "count": count
    })


def clean_orders():
    filepath = RAW_DIR / "orders.csv"

    df = pd.read_csv(
        filepath,
        dtype=str
    )

    original_rows = len(df)

    duplicate_count = df.duplicated(
        subset=["order_id"]
    ).sum()

    if duplicate_count > 0:
        add_issue(
            "Duplicate Orders",
            "Duplicate order IDs were removed.",
            duplicate_count
        )

        df = df.drop_duplicates(
            subset=["order_id"],
            keep="first"
        )

    missing_customer_ids = (
        df["customer_id"].isna()
        | (df["customer_id"].str.strip() == "")
    )

    missing_count = missing_customer_ids.sum()

    if missing_count > 0:
        add_issue(
            "Missing Customer IDs",
            "Missing customer IDs were retained as NULL because the order itself is still valid.",
            missing_count
        )

        df.loc[
            missing_customer_ids,
            "customer_id"
        ] = pd.NA

    original_dates = df["order_date"].copy()

    parsed_dates = pd.to_datetime(
        df["order_date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    missing_dates = parsed_dates.isna()

    parsed_dates.loc[missing_dates] = pd.to_datetime(
        df.loc[missing_dates, "order_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    invalid_date_count = parsed_dates.isna().sum()

    if invalid_date_count > 0:
        add_issue(
            "Invalid Order Dates",
            "Order dates that could not be parsed were converted to NULL.",
            invalid_date_count
        )

    fixed_date_count = (
        original_dates.notna()
        & parsed_dates.notna()
        & (
            original_dates
            != parsed_dates.dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    ).sum()

    if fixed_date_count > 0:
        add_issue(
            "Incorrect Date Format",
            "DD-MM-YYYY dates were converted to YYYY-MM-DD HH:MM:SS.",
            fixed_date_count
        )

    df["order_date"] = parsed_dates.dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    output_path = CLEAN_DIR / "orders_clean.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Orders cleaned: {original_rows} → {len(df)} rows"
    )

    return df


def clean_products():
    filepath = RAW_DIR / "products.csv"

    df = pd.read_csv(
        filepath,
        dtype=str
    )

    original_rows = len(df)

    duplicate_count = df.duplicated(
        subset=["product_id"]
    ).sum()

    if duplicate_count > 0:
        add_issue(
            "Duplicate Products",
            "Duplicate product IDs were removed.",
            duplicate_count
        )

        df = df.drop_duplicates(
            subset=["product_id"],
            keep="first"
        )

    original_names = df["product_name"].copy()

    df["product_name"] = (
        df["product_name"]
        .str.strip()
        .str.title()
    )

    changed_names = (
        original_names != df["product_name"]
    ).sum()

    if changed_names > 0:
        add_issue(
            "Messy Product Names",
            "Extra spaces were removed and product names were converted to title case.",
            changed_names
        )

    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    )

    invalid_prices = df["cost_price"].isna().sum()

    if invalid_prices > 0:
        add_issue(
            "Invalid Product Prices",
            "Invalid cost prices were converted to NULL.",
            invalid_prices
        )

    output_path = CLEAN_DIR / "products_clean.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Products cleaned: {original_rows} → {len(df)} rows"
    )

    return df


def validate_emails():
    filepath = RAW_DIR / "customers.csv"

    df = pd.read_csv(
        filepath,
        dtype=str
    )

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    valid_emails = df["email"].str.match(
        email_pattern,
        na=False
    )

    invalid_rows = df.loc[
        ~valid_emails
    ]

    invalid_customer_ids = (
        invalid_rows["customer_id"]
        .tolist()
    )

    invalid_count = len(
        invalid_customer_ids
    )

    if invalid_count > 0:
        add_issue(
            "Invalid Emails",
            "Invalid email addresses were identified and replaced with NULL.",
            invalid_count
        )

    df.loc[
        ~valid_emails,
        "email"
    ] = pd.NA

    duplicate_count = df.duplicated(
        subset=["customer_id"]
    ).sum()

    if duplicate_count > 0:
        add_issue(
            "Duplicate Customers",
            "Duplicate customer IDs were removed.",
            duplicate_count
        )

        df = df.drop_duplicates(
            subset=["customer_id"],
            keep="first"
        )

    output_path = CLEAN_DIR / "customers_clean.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Customers cleaned: {len(df)} rows"
    )

    return invalid_customer_ids


def clean_order_items():
    filepath = RAW_DIR / "order_items.csv"

    df = pd.read_csv(filepath)

    original_rows = len(df)

    duplicate_count = df.duplicated(
        subset=["item_id"]
    ).sum()

    if duplicate_count > 0:
        add_issue(
            "Duplicate Order Items",
            "Duplicate item IDs were removed.",
            duplicate_count
        )

        df = df.drop_duplicates(
            subset=["item_id"],
            keep="first"
        )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    df["discount_percent"] = pd.to_numeric(
        df["discount_percent"],
        errors="coerce"
    )

    invalid_discount = (
        (df["discount_percent"] < 0)
        | (df["discount_percent"] > 100)
    )

    invalid_discount_count = (
        invalid_discount.sum()
    )

    if invalid_discount_count > 0:
        add_issue(
            "Invalid Discounts",
            "Discount percentages outside 0-100 were set to NULL.",
            invalid_discount_count
        )

        df.loc[
            invalid_discount,
            "discount_percent"
        ] = pd.NA

    negative_quantity_count = (
        df["quantity"] < 0
    ).sum()

    if negative_quantity_count > 0:
        add_issue(
            "Negative Quantities",
            "Negative quantities were retained because they represent returns.",
            negative_quantity_count
        )

    output_path = CLEAN_DIR / "order_items_clean.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Order items cleaned: {original_rows} → {len(df)} rows"
    )

    return df


def check_referential_integrity():
    orders = pd.read_csv(
        CLEAN_DIR / "orders_clean.csv",
        dtype=str
    )

    order_items = pd.read_csv(
        CLEAN_DIR / "order_items_clean.csv",
        dtype=str
    )

    valid_order_ids = set(
        orders["order_id"].dropna()
    )

    invalid_items = order_items[
        ~order_items["order_id"].isin(
            valid_order_ids
        )
    ]

    invalid_count = len(
        invalid_items
    )

    if invalid_count > 0:
        add_issue(
            "Referential Integrity",
            "Order items referencing non-existent orders were removed.",
            invalid_count
        )

        order_items = order_items[
            order_items["order_id"].isin(
                valid_order_ids
            )
        ]

        order_items.to_csv(
            CLEAN_DIR / "order_items_clean.csv",
            index=False
        )

    else:
        add_issue(
            "Referential Integrity",
            "No invalid order references were found.",
            0
        )

    return invalid_items


def generate_issue_report():

    with open(
        ISSUE_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "E-COMMERCE DATA QUALITY REPORT\n"
        )

        file.write(
            "=" * 50 + "\n\n"
        )

        for issue in issues:

            file.write(
                f"Issue Type : {issue['issue_type']}\n"
            )

            file.write(
                f"Description: {issue['description']}\n"
            )

            file.write(
                f"Count      : {issue['count']}\n"
            )

            file.write(
                "-" * 50 + "\n"
            )

    print(
        f"\nIssue report created: {ISSUE_REPORT}"
    )


def main():

    print("\nStarting data cleaning...\n")

    clean_orders()

    clean_products()

    invalid_customer_ids = validate_emails()

    print(
        f"Invalid customer emails found: "
        f"{len(invalid_customer_ids)}"
    )

    clean_order_items()

    invalid_items = check_referential_integrity()

    print(
        f"Invalid order references found: "
        f"{len(invalid_items)}"
    )

    generate_issue_report()

    print(
        "\nData cleaning completed successfully!"
    )


if __name__ == "__main__":
    main()