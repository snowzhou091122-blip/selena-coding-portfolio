# Olist Data Dictionary

Source: [Olist work-at-olist-data](https://github.com/olist/work-at-olist-data/tree/master/datasets)  
Downloaded and profiled: 2026-07-18

## How to Read This Document

- **Grain** means what one row represents.
- **Primary/candidate key** means the field or field combination that uniquely identifies a row in this copy of the data.
- **Foreign key** means a field used to connect one table to another.
- Row counts and key uniqueness were verified with `scripts/profile_raw_data.py`.

## Table Summary

| Table | Rows | Grain | Primary or candidate key |
| --- | ---: | --- | --- |
| `olist_orders_dataset.csv` | 99,441 | One order | `order_id` |
| `olist_customers_dataset.csv` | 99,441 | One order-specific customer record | `customer_id` |
| `olist_order_reviews_dataset.csv` | 99,224 | One review record linked to an order | (`review_id`, `order_id`) |
| `olist_order_payments_dataset.csv` | 103,886 | One sequential payment record for an order | (`order_id`, `payment_sequential`) |
| `olist_order_items_dataset.csv` | 112,650 | One item line within an order | (`order_id`, `order_item_id`) |
| `olist_products_dataset.csv` | 32,951 | One product | `product_id` |
| `olist_sellers_dataset.csv` | 3,095 | One seller | `seller_id` |
| `product_category_name_translation.csv` | 71 | One Portuguese product-category translation | `product_category_name` |
| `olist_geolocation_dataset.csv` | 1,000,163 | One geographic coordinate observation for a ZIP prefix | No reliable single primary key |

## Core Relationships

```text
customers.customer_id
        |
        v
orders.customer_id
        |
        +---- order_items.order_id ---- products.product_id
        |                |
        |                +------------- sellers.seller_id
        |
        +---- order_payments.order_id
        |
        +---- order_reviews.order_id

products.product_category_name
        |
        v
product_category_name_translation.product_category_name
```

ZIP-code prefixes can connect customers and sellers to geolocation, but the geolocation table must be aggregated first because each prefix can appear many times.

## `olist_orders_dataset.csv`

**Grain:** one row per order.  
**Primary key:** `order_id` (unique in the downloaded data).  
**Foreign key:** `customer_id` -> `olist_customers_dataset.customer_id`.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `order_id` | Order identifier | Main key used to join orders to items, payments, and reviews |
| `customer_id` | Order-specific customer identifier | Joins to the customers table |
| `order_status` | Current/final order status | Use `delivered` when calculating actual delivery performance |
| `order_purchase_timestamp` | Time the customer placed the order | Supports order-month and seasonality analysis |
| `order_approved_at` | Time payment/order approval occurred | Can measure approval delay; 160 values are missing |
| `order_delivered_carrier_date` | Time the carrier received the order | 1,783 values are missing |
| `order_delivered_customer_date` | Actual customer delivery time | Required for delay calculations; 2,965 values are missing |
| `order_estimated_delivery_date` | Promised/estimated delivery date | Compare with actual delivery time to flag late orders |

**Planned derived fields:**

- `is_late = order_delivered_customer_date > order_estimated_delivery_date`
- `delay_days = order_delivered_customer_date - order_estimated_delivery_date`
- `purchase_month` from `order_purchase_timestamp`

## `olist_customers_dataset.csv`

**Grain:** one row per `customer_id`, which is an order-specific customer record.  
**Primary key:** `customer_id` (unique).  
**Important identity field:** `customer_unique_id` can repeat and represents the same real customer across different orders.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `customer_id` | Identifier attached to a particular order | Joins directly to `orders.customer_id` |
| `customer_unique_id` | Stable customer identifier across orders | Use this field when counting unique people or repeat customers |
| `customer_zip_code_prefix` | Customer ZIP-code prefix | Can support approximate geographic analysis |
| `customer_city` | Customer city | Compare delivery performance across cities |
| `customer_state` | Customer state abbreviation | Compare delivery performance across states |

**Important warning:** counting `customer_id` does not necessarily count unique people. Use `customer_unique_id` for that purpose.

## `olist_order_reviews_dataset.csv`

**Grain:** one review record associated with an order.  
**Candidate key:** (`review_id`, `order_id`) is unique in this data. `review_id` alone is not unique and has 814 duplicate-key rows.  
**Foreign key:** `order_id` -> `olist_orders_dataset.order_id`.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `review_id` | Review identifier | Must be used with `order_id` when a unique row key is needed |
| `order_id` | Reviewed order | Joins review outcomes to delivery performance |
| `review_score` | Customer rating, generally 1 through 5 | Main customer-satisfaction outcome |
| `review_comment_title` | Optional comment title | 87,656 values are missing |
| `review_comment_message` | Optional written review | 58,247 values are missing |
| `review_creation_date` | Review creation date | Supports timing checks |
| `review_answer_timestamp` | Timestamp when the review was answered/submitted | Supports response-time exploration |

**Planned derived field:** `is_low_rating = review_score IN (1, 2)`.

## `olist_order_payments_dataset.csv`

**Grain:** one sequential payment record for an order. An order can have more than one payment record.  
**Candidate key:** (`order_id`, `payment_sequential`) is unique.  
**Foreign key:** `order_id` -> `olist_orders_dataset.order_id`.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `order_id` | Paid order | Connects payment information to the order |
| `payment_sequential` | Sequence number of the payment record within an order | Distinguishes multiple payments for one order |
| `payment_type` | Payment method | Supports payment-method comparisons |
| `payment_installments` | Number of installments | Indicates installment use |
| `payment_value` | Value of this payment record | Sum by `order_id` before joining to an order-level table |

**Important warning:** joining payments directly to orders without aggregating can create multiple rows per order.

## `olist_order_items_dataset.csv`

**Grain:** one item line within an order.  
**Candidate key:** (`order_id`, `order_item_id`) is unique.  
**Foreign keys:** `order_id`, `product_id`, and `seller_id`.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `order_id` | Parent order | Joins to orders |
| `order_item_id` | Item sequence within the order | Distinguishes multiple item lines |
| `product_id` | Purchased product | Joins to products |
| `seller_id` | Seller fulfilling the item | Joins to sellers |
| `shipping_limit_date` | Seller shipping deadline | Can support fulfillment-delay analysis |
| `price` | Item price | Aggregate to order value or compare product groups |
| `freight_value` | Freight charged for the item | Aggregate to order freight cost |

**Important warning:** joining items directly to orders changes the grain from one row per order to one row per item.

## `olist_products_dataset.csv`

**Grain:** one product.  
**Primary key:** `product_id` (unique).

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `product_id` | Product identifier | Joins to order items |
| `product_category_name` | Product category in Portuguese | Joins to category translation; 610 values are missing |
| `product_name_lenght` | Product-name character count | Original source spelling is preserved |
| `product_description_lenght` | Product-description character count | Original source spelling is preserved |
| `product_photos_qty` | Number of product photos | Possible product-information feature |
| `product_weight_g` | Product weight in grams | Possible shipping/delivery feature; 2 values missing |
| `product_length_cm` | Product length in centimeters | Product-size feature; 2 values missing |
| `product_height_cm` | Product height in centimeters | Product-size feature; 2 values missing |
| `product_width_cm` | Product width in centimeters | Product-size feature; 2 values missing |

## `olist_sellers_dataset.csv`

**Grain:** one seller.  
**Primary key:** `seller_id` (unique).

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `seller_id` | Seller identifier | Joins to order items |
| `seller_zip_code_prefix` | Seller ZIP-code prefix | Approximate seller location |
| `seller_city` | Seller city | Compare seller-location performance |
| `seller_state` | Seller state abbreviation | Compare seller-location performance |

## `product_category_name_translation.csv`

**Grain:** one category translation.  
**Primary key:** `product_category_name` (unique).

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `product_category_name` | Portuguese category name | Joins to products |
| `product_category_name_english` | English category name | Makes charts and reporting easier to read |

## `olist_geolocation_dataset.csv`

**Grain:** one coordinate observation associated with a ZIP-code prefix, city, and state.  
**Primary key:** none declared; ZIP-code prefixes repeat.

| Field | Meaning | Why it matters |
| --- | --- | --- |
| `geolocation_zip_code_prefix` | ZIP-code prefix | Connects approximately to customer/seller ZIP prefixes after aggregation |
| `geolocation_lat` | Latitude | Mapping or distance calculations |
| `geolocation_lng` | Longitude | Mapping or distance calculations |
| `geolocation_city` | City | Geographic labeling |
| `geolocation_state` | State abbreviation | Geographic labeling |

**Important warning:** aggregate to one coordinate per ZIP prefix before joining. A direct join can multiply rows and corrupt rates and averages.

## Tables Needed for the First Analysis

The first delivery-and-rating analysis should begin with:

1. `orders` for estimated and actual delivery dates.
2. `reviews` for customer scores.
3. `customers` for customer location.
4. Aggregated `order_items` for price, freight, seller, and product identifiers.
5. `products`, category translation, and `sellers` for category and seller-location analysis.
6. `payments` only when payment value or payment method becomes part of a specific question.

Geolocation is optional for the first version and should not block the initial analysis.

