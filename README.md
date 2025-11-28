 Inventory, Purchase, and Sales Analysis and Optimization

This repository contains the code and analysis for project .The goal was to leverage transactional data to optimize inventory control and extract valuable business insights related to purchase and sales performance.

## Analysis Performed

1.  **Data Preparation:** Cleaning, merging, and feature engineering across all provided CSV files.
2.  **ABC Analysis:** Classification of inventory based on Gross Profit contribution (A, B, and C categories).
3.  **Demand Forecasting:** Time-series forecasting (ARIMA) for a top-selling product.
4.  **Inventory Optimization:** Calculation of Economic Order Quantity (EOQ) and Reorder Point (ROP).
5.  **Lead Time Analysis:** Assessment of supply chain efficiency and vendor performance.
6.  **Financial Insights:** Calculation of Inventory Turnover Ratio (ITR) and Gross Profit Margin (GPM) analysis.

## Repository Contents

| File Name | Description |
| :--- | :--- |
| `Slooze_Data_Science_Analytics_Report.md` | The final report summarizing the findings, recommendations, and next steps. |
| `data_preparation.py` | Script for initial data loading, cleaning, and merging. |
| `abc_analysis.py` | Script for performing the ABC inventory classification. |
| `demand_forecasting.py` | Script for time-series demand forecasting. |
| `inventory_optimization.py` | Script for calculating EOQ and ROP. |
| `lead_time_analysis.py` | Script for analyzing vendor lead times and payment lags. |
| `additional_insights.py` | Script for ITR, GPM, and city sales analysis. |
| `demand_forecast_plot.png` | Visualization of the demand forecast. |

## How to Run the Code Locally

### Prerequisites

You need Python 3.x installed.

### 1. Setup Environment

Install the required Python libraries:

\`\`\`bash
pip install pandas numpy statsmodels matplotlib
\`\`\`

### 2. Data Placement

Place the six original CSV files provided in the challenge into a directory named \`upload/\` in the same root folder as the Python scripts.

The required files are:
*   `2017PurchasePricesDec.csv`
*   `BegInvFINAL12312016.csv`
*   `EndInvFINAL12312016.csv`
*   `InvoicePurchases12312016.csv`
*   `PurchasesFINAL12312016.csv`
*   `SalesFINAL12312016.csv`

### 3. Execution

The scripts must be run sequentially as they rely on the output (cleaned CSV files) of the previous steps.

\`\`\`bash
# 1. Data Cleaning and Preparation
python3 data_preparation.py

# 2. ABC Analysis
python3 abc_analysis.py

# 3. Demand Forecasting (generates demand_forecast_plot.png)
python3 demand_forecasting.py

# 4. Inventory Optimization (EOQ/ROP)
python3 inventory_optimization.py

# 5. Lead Time Analysis
python3 lead_time_analysis.py

# 6. Additional Insights (ITR, GPM, City Sales)
python3 additional_insights.py
\`\`\`

After execution, the final report and all generated artifacts will be available in the root directory.

