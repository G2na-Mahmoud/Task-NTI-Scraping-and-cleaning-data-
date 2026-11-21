# Data Cleaning Task

## Overview
Cleaned five CSV datasets (`customers_master`, `new_daily_batch`, `orders`, `previous_days_summary`, and `products_master`) in VS Code using `pandas`, saving the cleaned versions while keeping raw data intact.

## Challenges & Solutions
- **Duplicate Rows:** Removed duplicate records in `orders` and `new_daily_batch` using `drop_duplicates()`.
- **Inconsistent Text Formatting & Whitespace:** Stripped leading/trailing spaces and standardized casing (`title()`) on text columns such as regions, segments, order statuses, and payment methods.
- **Missing Values & Date Types:** Converted date columns with `pd.to_datetime(..., errors="coerce")`, filled missing `Customer_ID` values with `"Unknown"`, imputed missing `Shipping_Cost` with the median, and filled missing `Unit_Price` from product pricing where available without blindly dropping valid records.