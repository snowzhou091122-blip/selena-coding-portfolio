from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"

# Step 1: load the raw orders table without changing the source file.
orders = pd.read_csv(RAW_FILE)

exact_duplicate_count = int(orders.duplicated().sum())
duplicate_order_id_count = int(orders["order_id"].duplicated().sum())

print("Step 1 - Duplicate check")
print(f"Rows: {len(orders):,}")
print(f"Exact duplicate rows: {exact_duplicate_count}")
print(f"Duplicate order_id values: {duplicate_order_id_count}")

# Step 2: convert timestamp text to pandas datetime values.
DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

parse_failures = {}
for column in DATE_COLUMNS:
    source_present = orders[column].notna()
    orders[column] = pd.to_datetime(orders[column], errors="coerce")
    parse_failures[column] = int(
        (source_present & orders[column].isna()).sum()
    )

print("\nStep 2 - Date conversion")
for column in DATE_COLUMNS:
    print(
        f"{column}: {orders[column].dtype}; "
        f"parse failures: {parse_failures[column]}"
    )

# Step 3: understand missing dates before deciding what to exclude.
missing_date_counts = orders[DATE_COLUMNS].isna().sum()
missing_customer_delivery_by_status = (
    orders.loc[orders["order_delivered_customer_date"].isna(), "order_status"]
    .value_counts()
    .sort_index()
)

delivered_count = int(orders["order_status"].eq("delivered").sum())
delivery_analysis_mask = (
    orders["order_status"].eq("delivered")
    & orders["order_delivered_customer_date"].notna()
    & orders["order_estimated_delivery_date"].notna()
)
delivery_analysis_count = int(delivery_analysis_mask.sum())

print("\nStep 3 - Missing-date check")
print("Missing values in each date column:")
print(missing_date_counts.to_string())
print("\nOrders missing customer delivery date, grouped by status:")
print(missing_customer_delivery_by_status.to_string())
print(f"\nDelivered orders: {delivered_count:,}")
print(f"Eligible for delivery analysis: {delivery_analysis_count:,}")
print(
    "Delivered orders excluded from delivery metrics because a required "
    f"date is missing: {delivered_count - delivery_analysis_count:,}"
)

# Step 4: calculate delivery metrics only where the required dates exist.
orders["delivery_analysis_eligible"] = delivery_analysis_mask
orders["delay_days"] = pd.NA
orders.loc[delivery_analysis_mask, "delay_days"] = (
    orders.loc[
        delivery_analysis_mask, "order_delivered_customer_date"
    ]
    - orders.loc[
        delivery_analysis_mask, "order_estimated_delivery_date"
    ]
).dt.total_seconds() / 86400
orders["delay_days"] = pd.to_numeric(orders["delay_days"])

orders["is_late"] = pd.Series(pd.NA, index=orders.index, dtype="boolean")
orders.loc[delivery_analysis_mask, "is_late"] = (
    orders.loc[delivery_analysis_mask, "delay_days"] > 0
)

# Keep date inconsistencies as flags so later analyses can decide whether
# those timestamps are relevant to a specific metric.
orders["flag_carrier_before_purchase"] = (
    orders["order_delivered_carrier_date"]
    < orders["order_purchase_timestamp"]
)
orders["flag_customer_before_carrier"] = (
    orders["order_delivered_customer_date"]
    < orders["order_delivered_carrier_date"]
)

late_count = int(orders.loc[delivery_analysis_mask, "is_late"].sum())
late_rate = late_count / delivery_analysis_count
eligible_delay_days = orders.loc[delivery_analysis_mask, "delay_days"]

print("\nStep 4 - Delivery metrics and anomaly flags")
print(f"Eligible delivery orders: {delivery_analysis_count:,}")
print(f"Late orders: {late_count:,}")
print(f"Late-delivery rate: {late_rate:.2%}")
print(f"Median delay_days: {eligible_delay_days.median():.2f}")
print(f"Minimum delay_days: {eligible_delay_days.min():.2f}")
print(f"Maximum delay_days: {eligible_delay_days.max():.2f}")
print(
    "Carrier timestamp before purchase: "
    f"{int(orders['flag_carrier_before_purchase'].sum()):,}"
)
print(
    "Customer delivery timestamp before carrier timestamp: "
    f"{int(orders['flag_customer_before_carrier'].sum()):,}"
)

# Step 5: save a separate processed table. The raw CSV remains unchanged.
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "olist_orders_cleaned.csv"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
orders.to_csv(
    PROCESSED_FILE,
    index=False,
    date_format="%Y-%m-%d %H:%M:%S",
)

saved_orders = pd.read_csv(PROCESSED_FILE)
if len(saved_orders) != len(orders):
    raise ValueError("Saved row count does not match the cleaned table")
if saved_orders["order_id"].duplicated().any():
    raise ValueError("Saved processed table contains duplicate order_id values")

print("\nStep 5 - Save processed table")
print(f"Saved file: {PROCESSED_FILE}")
print(f"Saved rows: {len(saved_orders):,}")
print(f"Saved columns: {len(saved_orders.columns)}")
print(
    "New analysis columns: delivery_analysis_eligible, delay_days, "
    "is_late, flag_carrier_before_purchase, "
    "flag_customer_before_carrier"
)
