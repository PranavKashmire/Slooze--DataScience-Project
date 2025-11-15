import pandas as pd
import os

# Load the cleaned dataframes
try:
    df_sales_master = pd.read_csv("/home/ubuntu/df_sales_master.csv")
    df_inventory_master = pd.read_csv("/home/ubuntu/df_inventory_master.csv")
except FileNotFoundError:
    print("Error: One or more cleaned data files not found. Please ensure previous steps are complete.")
    exit()

print("--- Starting Additional Insights Analysis ---")

# --- 1. Sales Trends by Store/City ---
df_store_sales = df_sales_master.groupby(['Store', 'VendorName']).agg(
    Total_Sales_Dollars=('SalesDollars', 'sum'),
    Total_Sales_Quantity=('SalesQuantity', 'sum')
).reset_index()

# Get City from inventory master
df_city_map = df_inventory_master[['Store', 'City']].drop_duplicates()
df_store_sales = pd.merge(df_store_sales, df_city_map, on='Store', how='left')

df_city_sales = df_store_sales.groupby('City').agg(
    Total_Sales_Dollars=('Total_Sales_Dollars', 'sum'),
    Total_Sales_Quantity=('Total_Sales_Quantity', 'sum')
).reset_index().sort_values(by='Total_Sales_Dollars', ascending=False)

print("\nTop 5 Cities by Total Sales Dollars:")
print(df_city_sales.head(5).to_markdown(index=False, floatfmt=".2f"))

# --- 2. Inventory Turnover Ratio (ITR) ---
# ITR = COGS / Average Inventory Value
# Average Inventory Value = (BegInvValue + EndInvValue) / 2

# Calculate Inventory Value (using Beg/End Price and onHand)
df_inventory_master['BegInvValue'] = df_inventory_master['Beg_onHand'] * df_inventory_master['Beg_Price']
df_inventory_master['EndInvValue'] = df_inventory_master['End_onHand'] * df_inventory_master['End_Price']

# Aggregate Inventory Value
total_beg_inv_value = df_inventory_master['BegInvValue'].sum()
total_end_inv_value = df_inventory_master['EndInvValue'].sum()
avg_inv_value = (total_beg_inv_value + total_end_inv_value) / 2

# Calculate Total COGS from sales master
total_cogs = df_sales_master['COGS'].sum()

# Calculate ITR
inventory_turnover_ratio = total_cogs / avg_inv_value

print(f"\nTotal COGS for 2016: ${total_cogs:,.2f}")
print(f"Average Inventory Value: ${avg_inv_value:,.2f}")
print(f"Overall Inventory Turnover Ratio (ITR): {inventory_turnover_ratio:.2f} times")

# --- 3. Top/Bottom Performing Products by Gross Profit Margin ---
# Calculate Gross Profit Margin (GPM) for each sale
df_sales_master['GPM'] = (df_sales_master['GrossProfit'] / df_sales_master['SalesDollars']) * 100

# Aggregate GPM by product
df_product_gpm = df_sales_master.groupby(['Brand', 'Description', 'Size']).agg(
    Avg_GPM=('GPM', 'mean'),
    Total_Sales_Dollars=('SalesDollars', 'sum'),
    Total_Sales_Quantity=('SalesQuantity', 'sum')
).reset_index()

# Filter out products with very low sales volume to avoid skewed GPM
min_sales_quantity = df_product_gpm['Total_Sales_Quantity'].quantile(0.5)
df_product_gpm_filtered = df_product_gpm[df_product_gpm['Total_Sales_Quantity'] >= min_sales_quantity]

df_top_gpm = df_product_gpm_filtered.sort_values(by='Avg_GPM', ascending=False).head(5)
df_bottom_gpm = df_product_gpm_filtered.sort_values(by='Avg_GPM', ascending=True).head(5)

print("\nTop 5 Products by Average Gross Profit Margin (GPM):")
print(df_top_gpm[['Description', 'Size', 'Avg_GPM', 'Total_Sales_Dollars']].to_markdown(index=False, floatfmt=".2f"))

print("\nBottom 5 Products by Average Gross Profit Margin (GPM):")
print(df_bottom_gpm[['Description', 'Size', 'Avg_GPM', 'Total_Sales_Dollars']].to_markdown(index=False, floatfmt=".2f"))

print("\n--- Additional Insights Analysis Complete ---")

