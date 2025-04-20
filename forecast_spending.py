import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime

# Step 1: Retrieve monthly totals from the database
def get_monthly_totals():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="finance_tracker"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Month", "Total"])

# Step 2: Forecast the next month's spending using linear regression
def forecast_next_month(df):
    df["MonthIndex"] = range(len(df))
    df["Total"] = df["Total"].astype(float)
    coeffs = np.polyfit(df["MonthIndex"], df["Total"], 1)
    slope, intercept = coeffs
    next_index = len(df)
    forecast_value = slope * next_index + intercept
    next_month_label = (datetime.now() + pd.DateOffset(months=1)).strftime("%Y-%m")
    return forecast_value, next_month_label

# Step 3: Process and plot the data
monthly_data = get_monthly_totals()
forecast_value, next_month_label = forecast_next_month(monthly_data)

monthly_data["Forecast"] = np.nan
forecast_df = pd.DataFrame(
    [[next_month_label, forecast_value, len(monthly_data), forecast_value]],
    columns=["Month", "Total", "MonthIndex", "Forecast"]
)

plot_data = pd.concat([monthly_data, forecast_df], ignore_index=True)

# Step 4: Visualization
plt.figure(figsize=(8, 5))
plt.plot(plot_data["Month"], plot_data["Total"], marker='o', label="Actual Spending")
plt.plot(plot_data["Month"], plot_data["Forecast"], linestyle='--', marker='x', color='orange', label="Forecast")
plt.title("Monthly Spending Forecast")
plt.xlabel("Month")
plt.ylabel("Total Spent ($)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
