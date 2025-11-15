import pandas as pd
import numpy as np
import os

# Load the cleaned dataframes
try:
    df_sales_master = pd.read_csv("/home/ubuntu/df_sales_master.csv")
    df_purchases_cleaned = pd.read_csv("/home/ubuntu/df_purchases_cleaned.csv")
    df_inventory_master = pd.read_csv("/home/ubuntu/df_inventory_master.csv")
    df_abc = pd.read_csv("/home/ubuntu/abc_analysis_results.csv")
except FileNotFoundError:
    print("Error: One or more cleaned data files not found. Please ensure previous steps are complete.")
    exit()

print("--- Starting EOQ and Reorder Point Analysis ---")

# --- 1. Calculate Annual Demand (D) and Average Daily Demand (D_avg) ---
# Assuming the data covers a full year (2016)
df_demand = df_sales_master.groupby(['Brand', 'Description', 'Size']).agg(
    Annual_Demand=('SalesQuantity', 'sum'),
    Total_Sales_Days=('SalesDate', lambda x: x.nunique())
).reset_index()

# Calculate Average Daily Demand (D_avg)
df_demand['Avg_Daily_Demand'] = df_demand['Annual_Demand'] / 365 # Using 365 days for the year

# --- 2. Determine Cost Parameters (Assumptions) ---
# Ordering Cost (S): Assumed cost per order (e.g., administrative, shipping fixed cost)
ORDERING_COST_S = 50.00 # $50 per order (Assumption)

# Holding Cost (H): Assumed as a percentage of the unit cost (PurchasePrice)
# Assuming 20% of the unit cost for holding (storage, insurance, obsolescence)
HOLDING_COST_PERCENTAGE = 0.20

# Merge with Purchase Price to get Unit Cost (C)
df_unit_cost = df_purchases_cleaned.groupby(['Brand', 'Description', 'Size'])['PurchasePrice'].mean().reset_index()
df_unit_cost = df_unit_cost.rename(columns={'PurchasePrice': 'Avg_Unit_Cost'})

df_eoq_rop = pd.merge(df_demand, df_unit_cost, on=['Brand', 'Description', 'Size'], how='left')

# Fill NaN Avg_Unit_Cost with 0 before calculating Holding Cost
df_eoq_rop['Avg_Unit_Cost'] = df_eoq_rop['Avg_Unit_Cost'].fillna(0)

# Calculate Holding Cost (H)
df_eoq_rop['Holding_Cost_H'] = df_eoq_rop['Avg_Unit_Cost'] * HOLDING_COST_PERCENTAGE

# --- 3. Calculate Economic Order Quantity (EOQ) ---
# EOQ = sqrt((2 * D * S) / H)
# Use a small epsilon to avoid division by zero if Holding_Cost_H is 0
epsilon = 1e-6
eoq_calc = np.sqrt(
    (2 * df_eoq_rop['Annual_Demand'] * ORDERING_COST_S) / (df_eoq_rop['Holding_Cost_H'] + epsilon)
).round(0)

# Replace NaN/Inf values with 0 (or a very large number if appropriate, but 0 is safer for inventory)
df_eoq_rop['EOQ'] = eoq_calc.fillna(0).replace([np.inf, -np.inf], 0).astype(int)

# --- 4. Calculate Lead Time (L) ---
# Calculate average lead time per product (InventoryId)
df_lead_time = df_purchases_cleaned.groupby(['Brand', 'Description', 'Size'])['LeadTime_Days'].mean().reset_index()
df_lead_time = df_lead_time.rename(columns={'LeadTime_Days': 'Avg_LeadTime_Days'})

df_eoq_rop = pd.merge(df_eoq_rop, df_lead_time, on=['Brand', 'Description', 'Size'], how='left')

# Fill missing lead times with the overall average lead time
overall_avg_lead_time = df_purchases_cleaned['LeadTime_Days'].mean()
df_eoq_rop['Avg_LeadTime_Days'] = df_eoq_rop['Avg_LeadTime_Days'].fillna(overall_avg_lead_time)

# --- 5. Calculate Reorder Point (ROP) ---
# ROP = Avg_Daily_Demand * Avg_LeadTime_Days (Safety Stock SS = 0 for simplicity)
rop_calc = (df_eoq_rop['Avg_Daily_Demand'] * df_eoq_rop['Avg_LeadTime_Days']).round(0)

# Replace NaN/Inf values with 0 before converting to integer
df_eoq_rop['Reorder_Point_ROP'] = rop_calc.fillna(0).replace([np.inf, -np.inf], 0).astype(int)

# --- 6. Merge with ABC Category for Context ---
df_eoq_rop = pd.merge(df_eoq_rop, df_abc[['Brand', 'Description', 'Size', 'ABC_Category']], on=['Brand', 'Description', 'Size'], how='left')

# Select and display key columns for the top 10 products
df_eoq_rop_top = df_eoq_rop.sort_values(by='Annual_Demand', ascending=False).head(10)

print("\nInventory Optimization Metrics (Top 10 Products):")
print(df_eoq_rop_top[[
    'Brand', 'Description', 'Size', 'ABC_Category', 'Annual_Demand',
    'Avg_Unit_Cost', 'Avg_LeadTime_Days', 'EOQ', 'Reorder_Point_ROP'
]].to_markdown(index=False, floatfmt=(".2f", ".2f", ".2f", ".0f")))

# Save the results
df_eoq_rop.to_csv("/home/ubuntu/inventory_optimization_metrics.csv", index=False)

print("\n--- EOQ and Reorder Point Analysis Complete. Results saved to inventory_optimization_metrics.csv ---")

