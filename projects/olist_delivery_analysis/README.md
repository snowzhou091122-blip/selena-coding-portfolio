# Olist Delivery Delay and Customer Review Analysis

## Project Status

Project framing, raw-data download, and the first data dictionary are complete. Analysis has not started yet.

- [Data dictionary](docs/data_dictionary.md)
- [Beginner guide in Chinese](docs/START_HERE_CN.md)
- [Raw-data source and download note](data/raw/README.md)
- [Raw-data profiling script](scripts/profile_raw_data.py)
- [Pandas data-inspection notebook](notebooks/01_data_inspection.ipynb)

## Data Source

The data comes from Olist's public Brazilian e-commerce dataset in the official
[work-at-olist-data repository](https://github.com/olist/work-at-olist-data/tree/master/datasets).
The original CSV files are kept locally in `data/raw/` and excluded from Git
because they are large. The source link and download date are documented in
[`data/raw/README.md`](data/raw/README.md).

## Audience

Olist e-commerce operations and customer experience teams.

## Business Problem

Which order, product, seller, and delivery factors are associated with late delivery and low customer ratings?

This project will identify patterns that can help an e-commerce operations team prioritize delivery and customer-experience improvements. The analysis will describe associations in the available data and will not claim that a factor causes a particular review score.

## Core Metrics

- Late-delivery rate: percentage of delivered orders whose actual delivery date is later than the estimated delivery date.
- Delay days: actual delivery date minus estimated delivery date.
- On-time delivery rate: percentage of delivered orders received on or before the estimated delivery date.
- Average review score: mean customer review score for the selected group of orders.
- Low-rating rate: percentage of reviewed orders with a score of 1 or 2.

## Analysis Questions

1. How do average review score and low-rating rate differ between late and on-time orders?
2. Which product categories, seller locations, and order months have the highest late-delivery rates?
3. How are delay days, freight cost, and order value associated with customer review scores?

## Planned Workflow

1. Download and document the public Olist dataset. **Complete**
2. Identify the tables and columns needed for orders, items, products, sellers, customers, and reviews. **Complete**
3. Clean dates, missing values, duplicate records, and inconsistent categories.
4. Build analysis-ready tables with SQL and Python/pandas.
5. Perform exploratory analysis and create decision-focused visualizations.
6. Summarize findings, limitations, and recommended next steps.

## Repository Structure

```text
olist_delivery_analysis/
├── README.md
├── data/
│   ├── raw/           # local source CSVs; ignored by Git
│   └── processed/     # future analysis-ready data
├── figures/           # charts for the final analysis
├── notebooks/
│   └── 01_data_inspection.ipynb
├── src/               # reusable cleaning and metric functions
├── docs/
│   ├── START_HERE_CN.md
│   └── data_dictionary.md
└── scripts/
    ├── inspect_orders_with_pandas.py
    └── profile_raw_data.py
```

The data contains no private user information. Large raw files are excluded from Git and linked to their public source instead.
