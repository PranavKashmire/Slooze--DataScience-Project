import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import os

# Load the cleaned sales master data
try:
    df_sales_master = pd.read_csv("/home/ubuntu/df_sales_master.csv")
except FileNotFoundError:
    print("Error: df_sales_master.csv not found. Please ensure data preparation is complete.")
    exit()

print("--- Starting Demand Forecasting ---")

# 1. Aggregate daily sales quantity for the entire company (for a general trend)
df_sales_master['SalesDate'] = pd.to_datetime(df_sales_master['SalesDate'])
df_daily_sales = df_sales_master.groupby('SalesDate')['SalesQuantity'].sum().reset_index()
df_daily_sales = df_daily_sales.set_index('SalesDate')

# Resample to weekly sales for smoother time series and better model performance
df_weekly_sales = df_daily_sales['SalesQuantity'].resample('W').sum()

# 2. Select a high-value product (Category A) for a more specific forecast
# We will use the product with the highest Gross Profit from the ABC analysis
try:
    df_abc = pd.read_csv("/home/ubuntu/abc_analysis_results.csv")
    top_product = df_abc.loc[df_abc['ABC_Category'] == 'A'].sort_values(by='TotalGrossProfit', ascending=False).iloc[0]
    top_brand = top_product['Brand']
    top_description = top_product['Description']
    top_size = top_product['Size']
    print(f"Forecasting for Top Product (A-Category): Brand {top_brand}, {top_description} ({top_size})")

    df_product_sales = df_sales_master[
        (df_sales_master['Brand'] == top_brand) &
        (df_sales_master['Description'] == top_description) &
        (df_sales_master['Size'] == top_size)
    ]
    df_product_daily_sales = df_product_sales.groupby('SalesDate')['SalesQuantity'].sum().reset_index()
    df_product_daily_sales = df_product_daily_sales.set_index('SalesDate')
    df_product_weekly_sales = df_product_daily_sales['SalesQuantity'].resample('W').sum()

except Exception as e:
    print(f"Could not load ABC results or select top product. Falling back to overall sales. Error: {e}")
    df_product_weekly_sales = df_weekly_sales

# 3. Time Series Modeling (ARIMA)
# We will use a simple ARIMA(1, 1, 1) model as a starting point for demonstration
# The data is from 2016, so we will forecast for the first 4 weeks of 2017 (4 steps)
try:
    # Fit the ARIMA model
    model = ARIMA(df_product_weekly_sales, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast the next 4 weeks
    forecast_steps = 4
    forecast = model_fit.forecast(steps=forecast_steps)

    # Create a DataFrame for the forecast results
    forecast_index = pd.date_range(start=df_product_weekly_sales.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='W')
    df_forecast = pd.DataFrame({'Forecasted_SalesQuantity': forecast.values.round(0)}, index=forecast_index)

    print("\nForecasted Weekly Sales Quantity (Next 4 Weeks):")
    print(df_forecast.to_markdown(numalign="left", stralign="left"))

    # 4. Plotting the results
    plt.figure(figsize=(12, 6))
    plt.plot(df_product_weekly_sales, label='Historical Weekly Sales')
    plt.plot(df_forecast, label='Forecasted Weekly Sales', color='red')
    plt.title(f'Demand Forecast for {top_description} (Weekly)')
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.savefig('/home/ubuntu/demand_forecast_plot.png')
    plt.close()

    print("\n--- Demand Forecasting Complete. Results saved to demand_forecast_plot.png ---")

except Exception as e:
    print(f"An error occurred during ARIMA modeling: {e}")

