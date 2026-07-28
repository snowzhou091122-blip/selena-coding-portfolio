from pathlib import Path

import pandas as pd


# Locate the orders CSV inside this project.
data_file = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "olist_orders_dataset.csv"
)

# Read the CSV into a pandas DataFrame named orders.
orders = pd.read_csv(data_file)

print("\n1. SHAPE: (rows, columns)")
print(orders.shape)

print("\n2. HEAD: first five rows")
print(orders.head())

print("\n3. DTYPES: data type of each column")
print(orders.dtypes)

print("\n4. ISNA: missing-value count in each column")
print(orders.isna().sum())
