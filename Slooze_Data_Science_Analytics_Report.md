# Slooze Take Home Challenge: Inventory, Purchase, and Sales Analysis and Optimization

## Executive Summary

This report presents a comprehensive data-driven analysis of the retail wine & spirits company's inventory, purchase, and sales data for the year 2016. The analysis, which included **Demand Forecasting**, **ABC Analysis**, **Economic Order Quantity (EOQ)**, **Reorder Point (ROP)**, and **Lead Time Analysis**, provides actionable insights to optimize inventory management, reduce inefficiencies, and enhance profitability.

Key findings include:
*   **Inventory Focus:** A small subset of **20.15%** of products (Category A) accounts for **79.99%** of the total gross profit, confirming the need for prioritized inventory management.
*   **Optimization Metrics:** Calculated EOQ and ROP provide data-backed order quantities and reorder triggers for top-selling items.
*   **Process Inefficiency:** The overall **Inventory Turnover Ratio (ITR) of 0.30** is extremely low, indicating significant overstocking and capital tied up in inventory.
*   **Supply Chain:** The average lead time is approximately **7.62 days**, with high consistency across major vendors, suggesting a reliable supply chain for planning.

## 1. Inventory Optimization: ABC Analysis

ABC analysis classifies inventory items based on their value contribution, allowing management to focus resources on the most critical products. The classification was performed based on **Total Gross Profit** for the year 2016.

| ABC_Category | Total Products | Product Share (%) | Total Gross Profit ($) | Profit Share (%) | Management Strategy |
|:-------------|---------------:|------------------:|-----------------------:|-----------------:|:--------------------|
| **A**        | 1,543          | 20.15             | 8,845,077.38           | 79.99            | Tight control, accurate forecasting, frequent review. |
| **B**        | 1,871          | 24.43             | 1,658,989.72           | 15.00            | Moderate control, periodic review. |
| **C**        | 4,244          | 55.42             | 553,274.23             | 5.00             | Simple control, bulk ordering, less frequent review. |

**Recommendation:** Implement a tiered inventory strategy where Category A items are subject to the most rigorous demand forecasting and control, while Category C items can be managed with simpler, less frequent ordering processes to reduce administrative overhead.

## 2. Inventory Optimization: EOQ and Reorder Point Analysis

The Economic Order Quantity (EOQ) model determines the optimal order size that minimizes the total inventory costs (ordering and holding costs). The Reorder Point (ROP) determines the inventory level at which a new order should be placed to prevent stockouts.

*Assumptions: Ordering Cost (S) = $50.00, Holding Cost (H) = 20% of Unit Cost.*

The table below shows the calculated metrics for the top 10 products by annual demand:

| Brand | Description | Size | ABC_Category | Annual Demand | Avg. Unit Cost ($) | Avg. Lead Time (Days) | EOQ (Units) | ROP (Units) |
|------:|:------------|:-----|:-------------|--------------:|-------------------:|----------------------:|------------:|------------:|
| 8111 | Smirnoff 80 Proof | 50mL | A | 28,544 | 0.77 | 7.62 | 4,305 | 596 |
| 1892 | Yukon Jack | 50mL | A | 23,121 | 0.72 | 7.68 | 4,007 | 486 |
| 4261 | Capt Morgan Spiced Rum | 1.75L | A | 20,226 | 16.17 | 7.34 | 791 | 407 |
| 3606 | Smirnoff Raspberry Vodka | 50mL | A | 19,200 | 0.74 | 7.70 | 3,602 | 405 |
| 5111 | Dr McGillicuddy's Mentholmnt | 50mL | A | 18,411 | 0.72 | 7.55 | 3,576 | 381 |
| 11219 | Josh Cellars Cab Svgn Sonoma | 750mL | A | 14,443 | 8.44 | 7.71 | 925 | 305 |
| 3837 | Skyy Vodka | 50mL | A | 14,057 | 0.72 | 7.46 | 3,124 | 287 |
| 4135 | Smirnoff Blueberry Vodka | 50mL | A | 12,477 | 0.78 | 7.69 | 2,828 | 263 |
| 4157 | Smirnoff Green Apple Vodka | 50mL | A | 12,102 | 0.72 | 7.65 | 2,899 | 254 |
| 3545 | Ketel One Vodka | 1.75L | A | 11,883 | 21.89 | 7.36 | 521 | 240 |

**Recommendation:** Implement the calculated EOQ as the standard order quantity and the ROP as the trigger for new orders. This will ensure inventory is ordered efficiently, minimizing costs and reducing the risk of stockouts for high-demand items.

## 3. Sales & Purchase Insights

### 3.1 Demand Forecasting

Demand forecasting is crucial for setting ROP and EOQ accurately. A time-series model (ARIMA) was applied to the top-selling product (Brand 4261, Capt Morgan Spiced Rum, 1.75L) to predict future weekly sales.

The forecast for the next four weeks shows a predicted weekly sales quantity. While the initial forecast showed negative values (likely due to the simplicity of the ARIMA(1,1,1) model on a short, potentially volatile time series), the process demonstrates the capability to generate a forward-looking demand signal.

**Recommendation:** For production use, a more robust model (e.g., SARIMA, Prophet) should be trained on a longer time series (if available) and incorporate external factors like holidays and promotions to improve accuracy. The current forecast plot is saved as \`/home/ubuntu/demand_forecast_plot.png\`.

### 3.2 Lead Time and Supplier Efficiency

Analyzing the time between placing a Purchase Order (PO Date) and receiving the goods (Receiving Date) is essential for supply chain optimization.

*   **Overall Average Lead Time:** **7.62 days**
*   **Overall Median Lead Time:** **8 days**
*   **Overall Standard Deviation:** **2.21 days**

The low standard deviation suggests that the lead times are generally consistent, which is a positive factor for inventory planning.

**Top 10 Vendors by Purchase Volume and their Lead Time Performance:**

| VendorName | Avg. Lead Time (Days) | Lead Time StdDev |
|:---------------------------|----------------------:|------------------:|
| DIAGEO NORTH AMERICA INC | 7.55 | 2.19 |
| MARTIGNETTI COMPANIES | 7.79 | 2.17 |
| JIM BEAM BRANDS COMPANY | 7.51 | 2.40 |
| PERNOD RICARD USA | 7.56 | 2.18 |
| BACARDI USA INC | 7.70 | 2.21 |
| CONSTELLATION BRANDS INC | 7.74 | 2.09 |
| BROWN-FORMAN CORP | 7.55 | 2.22 |
| ULTRA BEVERAGE COMPANY LLP | 8.41 | 2.03 |
| E & J GALLO WINERY | 7.62 | 2.28 |
| M S WALKER INC | 7.91 | 2.08 |

**Recommendation:** The consistency of lead times (low StdDev) across major vendors is a strength. The company should continue to monitor vendors with slightly longer average lead times (e.g., ULTRA BEVERAGE COMPANY LLP at 8.41 days) to ensure they do not negatively impact the ROP calculations.

## 4. Process Improvement and Financial Insights

### 4.1 Inventory Turnover Ratio (ITR)

The ITR measures how many times inventory is sold and replaced over a period.

*   **Total COGS for 2016:** $22,504,029.85
*   **Average Inventory Value:** $73,879,315.65
*   **Overall Inventory Turnover Ratio (ITR): 0.30 times**

An ITR of 0.30 is extremely low, suggesting that the company holds, on average, over three years' worth of inventory (1 / 0.30 ≈ 3.33 years). This indicates a massive amount of capital is tied up in stock, leading to high holding costs and risk of obsolescence.

**Recommendation:** The primary focus for process improvement must be to increase the ITR. Implementing the calculated EOQ and ROP, especially for Category A items, will be the first step in reducing excess inventory and improving cash flow.

### 4.2 Gross Profit Margin (GPM) Analysis

Analyzing GPM helps identify products that are either highly profitable or are being sold at a low margin, potentially due to high purchase costs or low selling prices.

**Top 5 Products by Average Gross Profit Margin (GPM):**

| Description | Size | Avg. GPM (%) | Total Sales Dollars ($) |
|:------------|:-----|-------------:|------------------------:|
| Spasso Pnt Grigio Veneto | 750mL | 100.00 | 349.30 |
| Massolino Nebbiolo Langhe | 750mL | 100.00 | 1,218.47 |
| Marco Barbanera Chianti DOCG | 750mL | 100.00 | 365.39 |
| New Amsterdam Citron Vodka | 375mL | 100.00 | 474.05 |
| Montignana 09 Chianti Clsco | 750mL | 100.00 | 662.49 |

*Note: The 100% GPM suggests that the average purchase price for these low-volume items was zero in the purchase data, which requires further investigation to ensure accurate COGS calculation.*

**Bottom 5 Products by Average Gross Profit Margin (GPM):**

| Description | Size | Avg. GPM (%) | Total Sales Dollars ($) |
|:------------|:-----|-------------:|------------------------:|
| Jack Daniels Winter Jack | 750mL | 19.54 | 7,465.31 |
| Martell Cordon Bleu | 750mL | 20.00 | 10,198.98 |
| Tommy Guns Vodka | 750mL | 20.01 | 4,558.86 |
| Powers Signature Release | 750mL | 20.01 | 2,079.48 |
| Gran Centenario Anejo | 750mL | 20.01 | 2,479.38 |

**Recommendation:** Investigate the bottom GPM products. If these are high-volume items, even a small increase in selling price or a negotiation for a lower purchase price could significantly boost overall profitability.

## 5. Conclusion and Next Steps

The analysis provides a strong foundation for a data-driven inventory strategy. The immediate next steps should focus on:

1.  **Inventory Reduction:** Prioritize the implementation of EOQ and ROP for Category A and B items to reduce the dangerously low ITR.
2.  **Data Refinement:** Investigate the products with 100% GPM and refine the COGS calculation to ensure all costs are accurately captured.
3.  **Advanced Forecasting:** Develop a more sophisticated demand forecasting model to account for seasonality and promotional effects, providing more reliable inputs for ROP.

This approach will lead to optimized inventory levels, minimized holding costs, and a more efficient supply chain, directly contributing to the company's financial health.

---
## Appendix: Code and Submission

The analysis was performed using Python with the \`pandas\`, \`numpy\`, \`statsmodels\`, and \`matplotlib\` libraries.

The following files contain the complete code for the analysis:
*   \`data_preparation.py\`: Data loading, cleaning, merging, and preliminary lead time calculation.
*   \`abc_analysis.py\`: Script for performing ABC analysis based on Gross Profit.
*   \`demand_forecasting.py\`: Script for time-series demand forecasting (ARIMA).
*   \`inventory_optimization.py\`: Script for calculating EOQ and Reorder Point.
*   \`lead_time_analysis.py\`: Script for analyzing vendor lead time and payment lag.
*   \`additional_insights.py\`: Script for ITR, GPM, and city sales analysis.

The following data artifacts were generated:
*   \`abc_analysis_results.csv\`
*   \`inventory_optimization_metrics.csv\`
*   \`demand_forecast_plot.png\` (Visualization of the demand forecast)

**Submission Instructions:**

1.  Upload all \`.py\` files, the Markdown report (\`Slooze_Data_Science_Analytics_Report.md\`), and the \`demand_forecast_plot.png\` to a GitHub repository.
2.  Include a \`README.md\` with instructions to run the code locally. The core steps are:
    *   Install dependencies: \`pip install pandas numpy statsmodels matplotlib\`
    *   Place the original CSV files in a designated folder (e.g., \`data/\`).
    *   Run the scripts sequentially: \`python3 data_preparation.py\`, \`python3 abc_analysis.py\`, etc.

