"""Reference queries C01 to C20: SQLite execution and independent check on the CSV files.

Run from the repository root (next to data/):
    python check_references.py

To export the 20 references to a new file:
    python check_references.py --export reference-td1-checked.csv

No API access and no external package. The database is opened read-only.
The export never overwrites an existing file.
The queries must be explained and cross-checked within the sub-group.
"""

import argparse
import csv
import sqlite3
import sys
from contextlib import closing
from datetime import date, datetime
from pathlib import Path


QUERIES = {
    "C01": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-03-01 00:00:00'
  AND o.date < '2026-06-01 00:00:00';
""",
    "C02": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25';
""",
    "C03": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date < '2026-07-01 00:00:00'
  AND o.product_id IN ('a', 'b', 'c');
""",
    "C04": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date < '2026-10-01 00:00:00';
""",
    "C05": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-06-01 00:00:00'
  AND o.date < '2026-06-02 00:00:00';
""",
    "C06": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2025-01-01 00:00:00'
  AND o.date < '2026-01-01 00:00:00';
""",
    "C07": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-05-31 00:00:00'
  AND o.date < '2026-06-01 00:00:00';
""",
    "C08": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-09-24'
  AND c.birth_date <= '2001-09-24';
""",
    "C09": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-09-26'
  AND c.birth_date <= '2001-09-26';
""",
    "C10": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE (CAST(strftime('%Y', o.date) AS INTEGER)
       - CAST(strftime('%Y', c.birth_date) AS INTEGER)
       - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date))) = 25;
""",
    "C11": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.birth_date > '2000-12-01'
  AND c.birth_date <= '2001-12-01';
""",
    "C12": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.product_id IN ('a', 'b', 'c');
""",
    "C13": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-04-01 00:00:00'
  AND o.date < '2026-05-01 00:00:00'
  AND o.product_id IN ('a', 'c');
""",
    "C14": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-10-01 00:00:00'
  AND o.date < '2026-12-01 00:00:00'
  AND o.product_id IN ('a', 'b', 'c');
""",
    "C15": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.date >= '2026-03-01 00:00:00'
  AND o.date < '2026-06-01 00:00:00'
  AND c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25';
""",
    "C16": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.product_id IN ('a', 'b', 'c')
  AND c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25';
""",
    "C17": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date < '2026-07-01 00:00:00'
  AND o.product_id IN ('a', 'b', 'c')
  AND c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25';
""",
    "C18": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.date >= '2026-05-01 00:00:00'
  AND o.date < '2026-06-01 00:00:00'
  AND (CAST(strftime('%Y', o.date) AS INTEGER)
       - CAST(strftime('%Y', c.birth_date) AS INTEGER)
       - (strftime('%m-%d', o.date) < strftime('%m-%d', c.birth_date))) = 25;
""",
    "C19": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.date >= '2026-09-01 00:00:00'
  AND o.date < '2026-10-01 00:00:00'
  AND o.product_id IN ('d')
  AND c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25';
""",
    "C20": """
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders AS o
JOIN product AS p ON p.product_id = o.product_id
WHERE o.date >= '2026-06-01 00:00:00'
  AND o.date < '2026-09-01 00:00:00';
""",
}

# Question parameters, for the separate computation on the CSV files.
PARAMETERS = {
    "C01": {"start": "2026-03-01", "end": "2026-06-01"},
    "C02": {"ref": "2026-09-25"},
    "C03": {"start": "2026-01-01", "end": "2026-07-01", "products": ["a","b","c"]},
    "C04": {"start": "2026-01-01", "end": "2026-10-01"},
    "C05": {"start": "2026-06-01", "end": "2026-06-02"},
    "C06": {"start": "2025-01-01", "end": "2026-01-01"},
    "C07": {"start": "2026-05-31", "end": "2026-06-01"},
    "C08": {"ref": "2026-09-24"},
    "C09": {"ref": "2026-09-26"},
    "C10": {"order_age": True},
    "C11": {"ref": "2026-12-01"},
    "C12": {"products": ["a","b","c"]},
    "C13": {"start": "2026-04-01", "end": "2026-05-01", "products": ["a","c"]},
    "C14": {"start": "2026-10-01", "end": "2026-12-01", "products": ["a","b","c"]},
    "C15": {"start": "2026-03-01", "end": "2026-06-01", "ref": "2026-09-25"},
    "C16": {"ref": "2026-09-25", "products": ["a","b","c"]},
    "C17": {"start": "2026-01-01", "end": "2026-07-01", "ref": "2026-09-25", "products": ["a","b","c"]},
    "C18": {"start": "2026-05-01", "end": "2026-06-01", "order_age": True},
    "C19": {"start": "2026-09-01", "end": "2026-10-01", "ref": "2026-09-25", "products": ["d"]},
    "C20": {"start": "2026-06-01", "end": "2026-09-01"},
}


def find_database(path):
    if path is not None:
        db = path.expanduser().resolve()
        if not db.is_file():
            raise FileNotFoundError(f"Database not found: {db}")
        return db
    for folder in (Path(__file__).resolve().parent, Path.cwd()):
        for relative in (Path("data/boutique.sqlite"), Path("kit-td1/data/boutique.sqlite")):
            db = (folder / relative).resolve()
            if db.is_file():
                return db
    raise FileNotFoundError(
        "Run this script from the repository root, next to data/, "
        'or pass --db "path/to/boutique.sqlite".'
    )


def run_sql(db):
    results = {}
    with closing(sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)) as connection:
        connection.execute("PRAGMA query_only = ON")
        for case, sql in QUERIES.items():
            cursor = connection.execute(sql)
            rows = cursor.fetchall()
            if (len(rows) != 1 or len(rows[0]) != 1
                    or cursor.description[0][0] != "revenue_cents"
                    or not isinstance(rows[0][0], int)):
                raise ValueError(f"{case}: expected a single integer revenue_cents value.")
            results[case] = rows[0][0]
    return results


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def completed_age(birth, day):
    birthday_not_reached = (day.month, day.day) < (birth.month, birth.day)
    return day.year - birth.year - birthday_not_reached


def compute_from_csv(folder):
    """No SQL: dictionary joins and a sum over the filtered CSV rows."""
    products = {
        row["product_id"]: int(row["price"])
        for row in read_csv(folder / "product.csv")
    }
    customers = {
        row["customer_id"]: date.fromisoformat(row["birth_date"])
        for row in read_csv(folder / "customers.csv")
    }
    results = dict.fromkeys(PARAMETERS, 0)
    for row in read_csv(folder / "orders.csv"):
        instant = datetime.fromisoformat(row["date"])
        birth = customers[row["customer_id"]]
        product = row["product_id"]
        amount = int(row["quantity_product"]) * products[product]
        for case, param in PARAMETERS.items():
            if "start" in param:
                start = datetime.fromisoformat(param["start"] + " 00:00:00")
                end = datetime.fromisoformat(param["end"] + " 00:00:00")
                if not start <= instant < end:
                    continue
            if "products" in param and product not in param["products"]:
                continue
            if "ref" in param:
                day = date.fromisoformat(param["ref"])
                if completed_age(birth, day) != 25:
                    continue
            if param.get("order_age") and completed_age(birth, instant.date()) != 25:
                continue
            results[case] += amount
    return results


def export(path, results):
    # Mode "x": never overwrites references already entered by the group.
    with path.open("x", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["case_id", "sql", "revenue_cents"])
        writer.writeheader()
        for case, sql in QUERIES.items():
            writer.writerow({
                "case_id": case,
                "sql": " ".join(sql.split()),
                "revenue_cents": results[case],
            })


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=Path, help="Optional path to boutique.sqlite.")
    parser.add_argument("--export", type=Path, help="New CSV file to create.")
    parser.add_argument("--sql-only", action="store_true", help="Skip the check on the CSV files.")
    args = parser.parse_args()
    try:
        db = find_database(args.db)
        sql = run_sql(db)
        print(f"Database: {db}\n")
        if args.sql_only:
            for case, value in sql.items():
                print(f"{case}: {value} cents")
            print("\nIndependent check on the CSV files not performed.")
        else:
            csv_results = compute_from_csv(db.parent)
            errors = []
            for case, value in sql.items():
                status = "OK" if value == csv_results[case] else "MISMATCH"
                print(f"{case}: SQL={value} | CSV={csv_results[case]} | {status}")
                if status != "OK":
                    errors.append(case)
            if errors:
                raise ValueError("Diverging results: " + ", ".join(errors))
            print("\n20/20 queries checked: same amounts in SQL and on the CSV files.")
        if args.export is not None:
            destination = args.export.expanduser().resolve()
            export(destination, sql)
            print(f"\nCSV created: {destination}")
        return 0
    except FileExistsError:
        print("Error: the export file already exists. Choose another name.", file=sys.stderr)
        return 1
    except (OSError, sqlite3.Error, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
