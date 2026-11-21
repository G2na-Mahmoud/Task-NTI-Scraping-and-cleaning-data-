from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent
out_root = base_dir / "cleaned_data"
out_root.mkdir(exist_ok=True)


def clean_text_cols(df, cols):
  for col in cols:
    if col in df.columns:
      df[col] = df[col].where(df[col].isna(), df[col].astype(str).str.strip())
  return df


# 1. customers_master.csv
customers = pd.read_csv(base_dir / "customers_master.csv").drop_duplicates()
customers = clean_text_cols(
    customers, ["Customer_ID", "Customer_Name", "Region", "Customer_Segment"]
)
customers["Region"] = customers["Region"].str.title()
customers["Customer_Segment"] = customers["Customer_Segment"].str.title()

# 2. products_master.csv
products = pd.read_csv(base_dir / "products_master.csv").drop_duplicates()
products = clean_text_cols(products, ["Product_ID", "Product_Name", "Category"])
products["Category"] = products["Category"].str.title()

# 3. previous_days_summary.csv
prev_summary = pd.read_csv(
    base_dir / "previous_days_summary.csv"
).drop_duplicates()
prev_summary["Date"] = pd.to_datetime(prev_summary["Date"], errors="coerce")


def clean_orders_df(df):
  df = df.drop_duplicates().copy()
  df = clean_text_cols(
      df,
      [
          "Order_ID",
          "Customer_ID",
          "Product_ID",
          "Order_Status",
          "Payment_Method",
      ],
  )
  df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
  df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], errors="coerce")
  df["Order_Status"] = df["Order_Status"].str.title()
  df["Payment_Method"] = df["Payment_Method"].str.title()

  df["Customer_ID"] = df["Customer_ID"].fillna("Unknown")
  if "Shipping_Cost" in df.columns:
    df["Shipping_Cost"] = pd.to_numeric(df["Shipping_Cost"], errors="coerce")
    df["Shipping_Cost"] = df["Shipping_Cost"].fillna(
        df["Shipping_Cost"].median()
    )

  if "Unit_Price" in df.columns and "Product_ID" in df.columns:
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    if "Unit_Cost" in products.columns:
      price_map = products.set_index("Product_ID")["Unit_Cost"]
      df["Unit_Price"] = df["Unit_Price"].fillna(df["Product_ID"].map(price_map))

  return df


orders = clean_orders_df(pd.read_csv(base_dir / "orders.csv"))
daily_batch = clean_orders_df(pd.read_csv(base_dir / "new_daily_batch.csv"))

# حفظ كل ملف نظيف جوه فولدر باسمه
cleaned_items = {
    "customers_master": ("customers_master_cleaned.csv", customers),
    "products_master": ("products_master_cleaned.csv", products),
    "previous_days_summary": ("previous_days_summary_cleaned.csv", prev_summary),
    "orders": ("orders_cleaned.csv", orders),
    "new_daily_batch": ("new_daily_batch_cleaned.csv", daily_batch),
}

for folder_name, (filename, df) in cleaned_items.items():
  sub_dir = out_root / folder_name
  sub_dir.mkdir(parents=True, exist_ok=True)
  df.to_csv(sub_dir / filename, index=False, encoding="utf-8-sig")
  print(f"Saved: {folder_name}/{filename} | Shape: {df.shape}")