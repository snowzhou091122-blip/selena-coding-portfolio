# Olist Project 1：从这里开始

你现在不用分析，也不用一次看完 9 张表。这个阶段只需要知道数据放在哪里，以及每张表代表什么。

## 四个必须懂的词

### Table（表）

一张 CSV 就像一张 Excel 工作表。例如 `olist_orders_dataset.csv` 是订单表。

### Row（行）

一行是一条记录。在 orders 表中，一行代表一个订单。

### Primary Key（主键）

主键是能唯一认出一行的字段。例如 `order_id` 像订单的身份证号码，不应该指向两个不同订单。

### Grain（粒度）

粒度回答：“这张表的一行到底代表什么？”

- orders：一行代表一个订单。
- payments：一行代表一次付款记录，一个订单可能有多行。
- order_items：一行代表订单中的一件商品，一个订单也可能有多行。

如果没有先弄清粒度就合并表，订单可能被重复计算。

## 先认识四张核心表

### 1. Orders

文件：`data/raw/olist_orders_dataset.csv`

- 一行：一个订单。
- 主键：`order_id`。
- 最重要字段：预计送达日期、实际送达日期、购买日期、订单状态。
- 用途：判断订单有没有晚到，以及晚了多少天。

### 2. Customers

文件：`data/raw/olist_customers_dataset.csv`

- 一行：一个订单对应的客户记录。
- 主键：`customer_id`。
- `customer_unique_id`：同一个真实客户跨订单的稳定编号。
- 用途：分析不同城市和州的配送表现。

### 3. Reviews

文件：`data/raw/olist_order_reviews_dataset.csv`

- 一行：一条订单评价记录。
- 组合键：`review_id + order_id`。
- 最重要字段：`review_score`。
- 用途：比较晚到和准时订单的评分。

### 4. Payments

文件：`data/raw/olist_order_payments_dataset.csv`

- 一行：一个订单的一次付款记录。
- 组合键：`order_id + payment_sequential`。
- 一个订单可能使用多次或多种付款，因此可能有多行。

## 你这次实际完成了什么

- 9 张官方 CSV 已保存在本地 `data/raw/`。
- 原始 CSV 已被 `.gitignore` 排除，不会上传到 GitHub。
- `docs/data_dictionary.md` 已列出每张表的行数、粒度、主键和关键字段。
- `scripts/profile_raw_data.py` 已验证行数、缺失值和候选键是否重复。

## 你的 10 分钟理解检查

读完后，不看答案，用中文回答：

1. orders 表的一行代表什么？
2. 为什么 `order_id` 像订单身份证？
3. 为什么 payments 表不能假设一个订单只有一行？
4. 哪两个日期可以判断订单是否晚到？

能回答这四题，就真正完成了“下载数据 + data dictionary”这项任务。

