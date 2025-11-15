import pandas as pd
import os

# Load the cleaned purchases data
try:
    df_purchases = pd.read_csv("/home/ubuntu/df_purchases_cleaned.csv")
except FileNotFoundError:
    print("Error: df_purchases_cleaned.csv not found. Please ensure data preparation is complete.")
    exit()

print("--- Starting Lead Time and Supplier Analysis ---")

# --- 1. Overall Lead Time Distribution ---
overall_avg_lead_time = df_purchases['LeadTime_Days'].mean()
overall_median_lead_time = df_purchases['LeadTime_Days'].median()
overall_std_lead_time = df_purchases['LeadTime_Days'].std()

print(f"Overall Average Lead Time (Receiving - PO Date): {overall_avg_lead_time:.2f} days")
print(f"Overall Median Lead Time: {overall_median_lead_time:.0f} days")
print(f"Overall Standard Deviation of Lead Time: {overall_std_lead_time:.2f} days")

# --- 2. Vendor Performance Analysis ---
# Group by Vendor and calculate average lead time and number of purchases
df_vendor_performance = df_purchases.groupby(['VendorNumber', 'VendorName']).agg(
    Avg_LeadTime_Days=('LeadTime_Days', 'mean'),
    Total_Purchases=('PONumber', 'nunique'),
    Total_Purchase_Dollars=('Dollars', 'sum')
).reset_index()

# Sort by Total Purchase Dollars to focus on major vendors
df_vendor_performance = df_vendor_performance.sort_values(by='Total_Purchase_Dollars', ascending=False)

print("\nTop 10 Vendors by Purchase Volume and their Lead Time Performance:")
print(df_vendor_performance.head(10).to_markdown(index=False, floatfmt=(".2f", ".0f", ".2f")))

# --- 3. Lead Time Consistency (Standard Deviation) ---
# Calculate the standard deviation of lead time for each vendor
df_vendor_std = df_purchases.groupby(['VendorNumber', 'VendorName'])['LeadTime_Days'].std().reset_index(name='LeadTime_StdDev')

# Merge with the performance data
df_vendor_performance = pd.merge(df_vendor_performance, df_vendor_std, on=['VendorNumber', 'VendorName'], how='left')

# Focus on the top 10 vendors by purchase volume and their consistency
df_vendor_consistency = df_vendor_performance.sort_values(by='Total_Purchase_Dollars', ascending=False).head(10)

print("\nLead Time Consistency for Top 10 Vendors (Lower StdDev is better):")
print(df_vendor_consistency[['VendorName', 'Avg_LeadTime_Days', 'LeadTime_StdDev']].to_markdown(index=False, floatfmt=".2f"))

# --- 4. Payment Lag Analysis (PayDate - InvoiceDate) ---
df_purchases['InvoiceDate'] = pd.to_datetime(df_purchases['InvoiceDate'])
df_purchases['PayDate'] = pd.to_datetime(df_purchases['PayDate'])
df_purchases['Payment_Lag_Days'] = (df_purchases['PayDate'] - df_purchases['InvoiceDate']).dt.days

df_payment_lag = df_purchases.groupby(['VendorNumber', 'VendorName'])['Payment_Lag_Days'].mean().reset_index(name='Avg_Payment_Lag_Days')
df_payment_lag = df_payment_lag.sort_values(by='Avg_Payment_Lag_Days', ascending=False)

print("\nTop 10 Vendors by Average Payment Lag (Days):")
print(df_payment_lag.head(10).to_markdown(index=False, floatfmt=".2f"))

print("\n--- Lead Time and Supplier Analysis Complete ---")

