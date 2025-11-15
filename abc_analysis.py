import pandas as pd
import os

# Load the cleaned sales master data
try:
    df_sales_master = pd.read_csv("/home/ubuntu/df_sales_master.csv")
except FileNotFoundError:
    print("Error: df_sales_master.csv not found. Please ensure data preparation is complete.")
    exit()

print("--- Starting ABC Analysis ---")

# 1. Aggregate Gross Profit by product (Brand and Description)
# Using Brand and Description as the unique product identifier for simplicity
df_product_profit = df_sales_master.groupby(['Brand', 'Description', 'Size'])['GrossProfit'].sum().reset_index()
df_product_profit = df_product_profit.rename(columns={'GrossProfit': 'TotalGrossProfit'})

# 2. Sort in descending order of Total Gross Profit
df_product_profit = df_product_profit.sort_values(by='TotalGrossProfit', ascending=False).reset_index(drop=True)

# 3. Calculate cumulative percentage of Gross Profit
df_product_profit['CumulativeProfit'] = df_product_profit['TotalGrossProfit'].cumsum()
df_product_profit['ProfitPercentage'] = df_product_profit['TotalGrossProfit'] / df_product_profit['TotalGrossProfit'].sum()
df_product_profit['CumulativeProfitPercentage'] = df_product_profit['ProfitPercentage'].cumsum()

# 4. Assign ABC Categories
def assign_abc(cumulative_percentage):
    if cumulative_percentage <= 0.80:
        return 'A' # High Value - Top 80% of profit
    elif cumulative_percentage <= 0.95:
        return 'B' # Moderate Value - Next 15% of profit
    else:
        return 'C' # Low Value - Remaining 5% of profit

df_product_profit['ABC_Category'] = df_product_profit['CumulativeProfitPercentage'].apply(assign_abc)

# Display summary statistics for the categories
abc_summary = df_product_profit.groupby('ABC_Category').agg(
    Total_Products=('Brand', 'count'),
    Total_Profit=('TotalGrossProfit', 'sum'),
    Min_Profit=('TotalGrossProfit', 'min'),
    Max_Profit=('TotalGrossProfit', 'max')
).reset_index()

total_profit = abc_summary['Total_Profit'].sum()
abc_summary['Profit_Share'] = (abc_summary['Total_Profit'] / total_profit) * 100
abc_summary['Product_Share'] = (abc_summary['Total_Products'] / df_product_profit.shape[0]) * 100

print("\nABC Analysis Summary:")
print(abc_summary.sort_values(by='Profit_Share', ascending=False).to_markdown(index=False, floatfmt=".2f"))

# Save the detailed ABC analysis results
df_product_profit.to_csv("/home/ubuntu/abc_analysis_results.csv", index=False)

print("\n--- ABC Analysis Complete. Results saved to abc_analysis_results.csv ---")

