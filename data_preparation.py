import pandas as pd
import os

# Directory where the uploaded files are located
upload_dir = "/home/ubuntu/upload"

# Load DataFrames
try:
    df_beg_inv = pd.read_csv(os.path.join(upload_dir, "BegInvFINAL12312016.csv"))
    df_end_inv = pd.read_csv(os.path.join(upload_dir, "EndInvFINAL12312016.csv"))
    df_purchases = pd.read_csv(os.path.join(upload_dir, "PurchasesFINAL12312016.csv"))
    df_sales = pd.read_csv(os.path.join(upload_dir, "SalesFINAL12312016.csv"))
    df_prices = pd.read_csv(os.path.join(upload_dir, "2017PurchasePricesDec.csv"))
    df_invoice = pd.read_csv(os.path.join(upload_dir, "InvoicePurchases12312016.csv"))
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

print("--- Starting Data Cleaning and Preparation ---")

# --- 1. Inventory Data Cleaning and Merging ---
# Rename columns for clarity and merging
df_beg_inv = df_beg_inv.rename(columns={'onHand': 'Beg_onHand', 'Price': 'Beg_Price'})
df_end_inv = df_end_inv.rename(columns={'onHand': 'End_onHand', 'Price': 'End_Price'})

# Handle missing 'City' in EndInvFINAL12312016.csv by filling from BegInvFINAL12312016.csv
city_map = df_beg_inv[['Store', 'City']].drop_duplicates().set_index('Store')['City'].to_dict()
df_end_inv['City'] = df_end_inv.apply(lambda row: row['City'] if pd.notna(row['City']) else city_map.get(row['Store']), axis=1)

# Merge beginning and ending inventory to calculate consumption/turnover
inventory_cols = ['InventoryId', 'Store', 'City', 'Brand', 'Description', 'Size']
df_inventory = pd.merge(
    df_beg_inv[inventory_cols + ['Beg_onHand', 'Beg_Price']],
    df_end_inv[inventory_cols + ['End_onHand', 'End_Price']],
    on=inventory_cols,
    how='outer'
).fillna(0)

# Calculate Average Inventory Price (simple average of beg and end price)
df_inventory['Avg_Price'] = (df_inventory['Beg_Price'] + df_inventory['End_Price']) / 2

# --- 2. Sales Data Cleaning ---
# Convert SalesDate to datetime
df_sales['SalesDate'] = pd.to_datetime(df_sales['SalesDate'])
# Calculate Gross Margin (assuming SalesDollars is Revenue and we need a cost)
# We will use the PurchasePrice from the PurchasesFINAL data later for a more accurate COGS.
# For now, we'll focus on clean sales data.

# --- 3. Purchases Data Cleaning ---
# Convert date columns to datetime
date_cols = ['PODate', 'ReceivingDate', 'InvoiceDate', 'PayDate']
for col in date_cols:
    df_purchases[col] = pd.to_datetime(df_purchases[col], errors='coerce')

# Handle missing 'Size' in PurchasesFINAL12312016.csv by filling from SalesFINAL12312016.csv
size_map = df_sales[['Brand', 'Size']].drop_duplicates().set_index('Brand')['Size'].to_dict()
df_purchases['Size'] = df_purchases.apply(lambda row: row['Size'] if pd.notna(row['Size']) else size_map.get(row['Brand']), axis=1)
df_purchases = df_purchases.dropna(subset=['Size']) # Drop remaining few NaNs if any

# --- 4. Lead Time Calculation (Preliminary) ---
# Calculate Lead Time in days: ReceivingDate - PODate
df_purchases['LeadTime_Days'] = (df_purchases['ReceivingDate'] - df_purchases['PODate']).dt.days

# --- 5. Final Merged Data for Analysis ---
# Merge Sales and Inventory to get a comprehensive view of product performance
# We will use the InventoryId to link sales to the product master data (inventory)
df_sales_master = pd.merge(
    df_sales,
    df_inventory[['InventoryId', 'Beg_onHand', 'End_onHand', 'Avg_Price']],
    on='InventoryId',
    how='left'
)

# Calculate Cost of Goods Sold (COGS) for sales.
# This is a simplification: using the average purchase price from the Purchases data.
# First, calculate the average purchase price per Brand/Size from the Purchases data.
df_avg_purchase_price = df_purchases.groupby(['Brand', 'Size'])['PurchasePrice'].mean().reset_index(name='Avg_PurchasePrice')

# Merge the average purchase price into the sales master data
df_sales_master = pd.merge(
    df_sales_master,
    df_avg_purchase_price,
    on=['Brand', 'Size'],
    how='left'
)

# Fill any remaining missing Avg_PurchasePrice with the SalesPrice as a last resort, or 0
df_sales_master['Avg_PurchasePrice'] = df_sales_master['Avg_PurchasePrice'].fillna(0)

# Calculate COGS and Gross Profit
df_sales_master['COGS'] = df_sales_master['SalesQuantity'] * df_sales_master['Avg_PurchasePrice']
df_sales_master['GrossProfit'] = df_sales_master['SalesDollars'] - df_sales_master['COGS']

# Save the cleaned and merged dataframes for subsequent phases
df_sales_master.to_csv("/home/ubuntu/df_sales_master.csv", index=False)
df_purchases.to_csv("/home/ubuntu/df_purchases_cleaned.csv", index=False)
df_inventory.to_csv("/home/ubuntu/df_inventory_master.csv", index=False)

print(f"Cleaned Sales Master Data Shape: {df_sales_master.shape}")
print(f"Cleaned Purchases Data Shape: {df_purchases.shape}")
print(f"Cleaned Inventory Master Data Shape: {df_inventory.shape}")
print("--- Data Cleaning and Preparation Complete ---")

