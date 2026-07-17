# Olist Delivery Delay and Customer Review Analysis

## Project Status

Project framing in progress. Data has not been downloaded or analyzed yet.

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

1. Download and document the public Olist dataset.
2. Identify the tables and columns needed for orders, items, products, sellers, customers, and reviews.
3. Clean dates, missing values, duplicate records, and inconsistent categories.
4. Build analysis-ready tables with SQL and Python/pandas.
5. Perform exploratory analysis and create decision-focused visualizations.
6. Summarize findings, limitations, and recommended next steps.

## Planned Repository Structure

```text
olist_delivery_analysis/
|-- README.md
|-- data/
|-- notebooks/
|-- sql/
`-- figures/
```

Large raw data files will be excluded from GitHub and linked to their public source instead.
