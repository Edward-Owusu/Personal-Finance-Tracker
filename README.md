# 💰 Personal Finance Tracker

A sleek, user-friendly desktop application built with Python and Tkinter that helps users track daily expenses, set monthly budgets, visualize spending habits, and export data to CSV — all stored in a local MySQL database.

---

## 📌 Project Description

The **Personal Finance Tracker** is a Python-based application that empowers individuals to manage their finances effectively. It supports input of daily expenses, categorization of spending, real-time pie chart visualization, and a monthly budget check system. It also features export functionality for offline analysis.

---

## 🎯 Purpose & Value

- 🧾 Track your daily and monthly expenses
- 📊 View colorful pie charts to analyze where your money goes
- 🧠 Stay within your budget using the budget check feature
- 📤 Export all expense data into a clean CSV file
- 💡 Simplified interface built with usability and accessibility in mind

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **Tkinter** – Graphical User Interface (GUI)
- **MySQL** – Data storage backend
- **Matplotlib** – Data visualization (pie chart)
- **Pandas** – CSV export handling
- **Pillow** – Optional: background image support (if used)

---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/Edward-Owusu/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker


## AI Feature: Spending Forecast

This project includes a basic AI/data insight feature that forecasts your next month's spending using linear regression. It analyzes past monthly expenses and generates a predicted total for the upcoming month.

### 🧠 How It Works:
- Uses `pandas`, `numpy`, and `matplotlib`.
- Fetches monthly totals from the MySQL database.
- Applies linear regression to project future spending.
- Visualizes actual and predicted spending in a line chart.

### 📊 Forecast Chart:
![Spending Forecast](Screenshots/ai_forecast_output.jpg)

