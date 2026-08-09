import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "ecommerce.db"


def run_sql_file(sql_file):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    sql_path = BASE_DIR / "sql" / sql_file

    with open(sql_path, "r", encoding="utf-8") as file:
        sql = file.read()

    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    for number, statement in enumerate(statements, start=1):
        cursor = connection.execute(statement)
        rows = cursor.fetchall()

        print(f"\n{'=' * 70}")
        print(f"QUERY {number}")
        print("=" * 70)

        if not rows:
            print("No results found.")
            continue

        columns = rows[0].keys()

        print(" | ".join(columns))
        print("-" * 70)

        for row in rows:
            print(
                " | ".join(
                    str(row[column])
                    for column in columns
                )
            )

    connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts\\run_sql.py <sql_file>")
        sys.exit(1)

    run_sql_file(sys.argv[1])