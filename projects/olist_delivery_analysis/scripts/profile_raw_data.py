"""Profile Olist raw CSV files using only Python's standard library."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

KEYS = {
    "olist_customers_dataset.csv": ("customer_id",),
    "olist_geolocation_dataset.csv": (),
    "olist_order_items_dataset.csv": ("order_id", "order_item_id"),
    "olist_order_payments_dataset.csv": ("order_id", "payment_sequential"),
    "olist_order_reviews_dataset.csv": ("review_id", "order_id"),
    "olist_orders_dataset.csv": ("order_id",),
    "olist_products_dataset.csv": ("product_id",),
    "olist_sellers_dataset.csv": ("seller_id",),
    "product_category_name_translation.csv": ("product_category_name",),
}


def profile_csv(path: Path, key_columns: tuple[str, ...]) -> dict[str, object]:
    row_count = 0
    columns: list[str] = []
    missing: Counter[str] = Counter()
    seen_keys: set[tuple[str, ...]] = set()
    duplicate_key_rows = 0

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []

        for row in reader:
            row_count += 1
            for column in columns:
                if row.get(column, "") == "":
                    missing[column] += 1

            if key_columns:
                key = tuple(row[column] for column in key_columns)
                if key in seen_keys:
                    duplicate_key_rows += 1
                else:
                    seen_keys.add(key)

    return {
        "file": path.name,
        "rows": row_count,
        "columns": columns,
        "key_columns": key_columns,
        "duplicate_key_rows": duplicate_key_rows,
        "missing": missing,
    }


def main() -> None:
    for filename, key_columns in KEYS.items():
        result = profile_csv(RAW_DIR / filename, key_columns)
        key_label = ", ".join(key_columns) if key_columns else "none declared"
        missing_summary = ", ".join(
            f"{column}={count}"
            for column, count in result["missing"].most_common()
            if count
        ) or "none"

        print(f"\n{result['file']}")
        print(f"  rows: {result['rows']:,}")
        print(f"  columns: {', '.join(result['columns'])}")
        print(f"  candidate key: {key_label}")
        print(f"  duplicate candidate-key rows: {result['duplicate_key_rows']:,}")
        print(f"  missing values: {missing_summary}")


if __name__ == "__main__":
    main()
