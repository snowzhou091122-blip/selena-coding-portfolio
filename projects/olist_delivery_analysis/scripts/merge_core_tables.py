from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

orders = pd.read_csv(PROCESSED_DIR / "olist_orders_cleaned.csv")
customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")

print("Step 1 - Load the four core tables")
print(f"orders: {orders.shape}")
print(f"customers: {customers.shape}")
print(f"reviews: {reviews.shape}")
print(f"payments: {payments.shape}")

payments_by_order = (
    payments.groupby("order_id", as_index=False)
    .agg(
        total_payment=("payment_value", "sum"),
        payment_count=("payment_sequential", "count"),
    )
)

print("\nStep 2 - Aggregate payments to one row per order")
print(f"Raw payment rows: {len(payments):,}")
print(f"Orders with payment records: {len(payments_by_order):,}")
print(
    "Duplicate order_id values after aggregation: "
    f"{payments_by_order['order_id'].duplicated().sum():,}"
)

reviews_by_order = (
    reviews.groupby("order_id", as_index=False)
    .agg(
        average_review_score=("review_score", "mean"),
        review_count=("review_score", "count"),
    )
)

print("\nStep 3 - Aggregate reviews to one row per order")
print(f"Raw review rows: {len(reviews):,}")
print(f"Orders with review records: {len(reviews_by_order):,}")
print(
    "Duplicate order_id values after aggregation: "
    f"{reviews_by_order['order_id'].duplicated().sum():,}"
)

merged_orders = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)

print("\nStep 4 - Merge customers into orders")
print(f"Rows before merge: {len(orders):,}")
print(f"Rows after merge: {len(merged_orders):,}")
print(
    "Duplicate order_id values after merge: "
    f"{merged_orders['order_id'].duplicated().sum():,}"
)
print(
    "Orders missing customer data: "
    f"{merged_orders['customer_unique_id'].isna().sum():,}"
)

rows_before_reviews = len(merged_orders)
merged_orders = merged_orders.merge(
    reviews_by_order,
    on="order_id",
    how="left",
    validate="one_to_one",
)

print("\nStep 5 - Merge reviews into orders")
print(f"Rows before merge: {rows_before_reviews:,}")
print(f"Rows after merge: {len(merged_orders):,}")
print(
    "Duplicate order_id values after merge: "
    f"{merged_orders['order_id'].duplicated().sum():,}"
)
print(
    "Orders missing review data: "
    f"{merged_orders['average_review_score'].isna().sum():,}"
)

rows_before_payments = len(merged_orders)
merged_orders = merged_orders.merge(
    payments_by_order,
    on="order_id",
    how="left",
    validate="one_to_one",
)

print("\nStep 6 - Merge payments into orders")
print(f"Rows before merge: {rows_before_payments:,}")
print(f"Rows after merge: {len(merged_orders):,}")
print(
    "Duplicate order_id values after merge: "
    f"{merged_orders['order_id'].duplicated().sum():,}"
)
print(
    "Orders missing payment data: "
    f"{merged_orders['total_payment'].isna().sum():,}"
)

if len(merged_orders) != len(orders):
    raise ValueError("Merged row count does not match the orders table")
if merged_orders["order_id"].duplicated().any():
    raise ValueError("Merged table contains duplicate order_id values")

output_file = PROCESSED_DIR / "olist_orders_customers_reviews_payments.csv"
merged_orders.to_csv(output_file, index=False)

print("\nStep 7 - Save the analysis-ready table")
print(f"Saved file: {output_file}")
print(f"Saved rows: {len(merged_orders):,}")
print(f"Saved columns: {len(merged_orders.columns)}")
