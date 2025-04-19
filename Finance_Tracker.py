"""
Finance_Tracker.py
Personal Finance Tracker application for tracking daily and monthly expenses.
Built with Python, Tkinter, MySQL, and Matplotlib.
"""


import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from tkinter import filedialog
import pandas as pd  # <-- Add this line here




def add_expense():
    pass  # Replace with your function logic

def clear_fields():
    pass  # Replace with your function logic

def delete_expense():
    pass  # Replace with your function logic

def load_expenses():
    pass  # Replace with your function logic

def show_chart():
    pass  # Replace with your function logic

def check_budget():
    pass  # Replace with your function logic

def calculate_daily_expenses():
    pass  # Replace with your function logic

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")])
    if not file_path:
        return


# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # Replace with your MySQL root password
        database="finance_tracker"
    )


# Create table if not exists
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            time TIME NOT NULL,
            category VARCHAR(50) NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_db()


# Function to calculate daily expenses
def calculate_daily_expenses():
    """Fetches and displays today's total expenses."""
    print("🔹 Checking today's expenses...")  # Debugging

    today = datetime.now().strftime("%Y-%m-%d")  # Get current date

    # Connect to database and fetch total expenses for today
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date = %s", (today,))
    total_spent = cursor.fetchone()[0]  # Fetch total amount spent

    conn.close()

    # If no expenses recorded, set total spent to 0
    if total_spent is None:
        total_spent = 0.0

    print(f"✅ Total spent today: {total_spent}")  # Debugging

    # Show notification
    messagebox.showinfo("Daily Expenses", f"Your total expenses for today ({today}) is: ${total_spent:.2f}")


# Function to add an expense
def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    description = description_entry.get()
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    if not amount:
        messagebox.showerror("Error", "Amount is required!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, time, category, amount, description) VALUES (%s, %s, %s, %s, %s)",
                       (date, time, category, amount, description))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expense added successfully!")
        load_expenses()
        clear_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


# Function to delete an expense
def delete_expense():
    selected_item = tree.selection()
    
    if not selected_item:
        messagebox.showerror("Error", "Please select an entry to delete")
        return
    
    item = tree.item(selected_item)
    values = item["values"]
    
    if len(values) < 5:
        messagebox.showerror("Error", "Invalid selection")
        return

    date, time, category, amount, description = values  # Extracting values correctly

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE date=%s AND time=%s AND category=%s AND amount=%s AND description=%s",
                       (date, time, category, amount, description))
        conn.commit()
        conn.close()

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Expense deleted successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    
    # Function to check spending against the budget
def check_budget():
    """Checks if total expenses exceed, meet, or are within the monthly budget."""
    print("🔹 check_budget() function is called.")  # Debugging

    month = datetime.now().strftime("%Y-%m")  # Get the current year-month
    budget_amount = monthly_budget_entry.get()  # Get user input budget

    print(f"🔹 Entered budget amount: {budget_amount}")  # Debugging

    # Validate if the budget is entered
    if not budget_amount:
        messagebox.showerror("Error", "Please enter a monthly budget amount!")
        print("⚠️ No budget entered.")  # Debugging
        return

    try:
        budget_amount = float(budget_amount)  # Convert to float for comparison
    except ValueError:
        messagebox.showerror("Error", "Invalid budget amount! Enter a valid number.")
        print("⚠️ Budget amount is not a valid number.")  # Debugging
        return

    # Connect to database and fetch total expenses for the current month
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE %s", (month + '%',))
    total_spent = cursor.fetchone()[0]  # Get total spent

    # If no expenses recorded, set total spent to 0
    if total_spent is None:
        total_spent = 0.0
    else:
        total_spent = float(total_spent)  # ✅ Convert to float to avoid type mismatch

    print(f"✅ Total spent this month: {total_spent}")  # Debugging
    conn.close()

    # Compare spending with the budget and show appropriate notification
    if total_spent > budget_amount:
        print("⚠️ Overspending detected.")  # Debugging
        messagebox.showwarning("Overspending Alert", 
                               f"You have exceeded your monthly budget!\n\n"
                               f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}\n"
                               f"Overspent by: ${total_spent - budget_amount:.2f}")
    elif total_spent == budget_amount:
        print("✅ Budget exactly matched.")  # Debugging
        messagebox.showinfo("Budget Status", 
                            f"You have spent exactly your budget.\n\n"
                            f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}")
    else:
        remaining = budget_amount - total_spent
        print("✅ Budget is within limit.")  # Debugging
        messagebox.showinfo("Budget Status", 
                            f"You are within budget.\n\n"
                            f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}\n"
                            f"Remaining: ${remaining:.2f}")

    # Compare spending with budget
    if total_spent > budget_amount:
        messagebox.showwarning("Overspending Alert", f"You have exceeded your monthly budget!\n\n"
                                                     f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}")
    elif total_spent == budget_amount:
        messagebox.showinfo("Budget Status", f"You have spent exactly your budget.\n\n"
                                             f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}")
    else:
        remaining = budget_amount - total_spent
        messagebox.showinfo("Budget Status", f"You are within budget.\n\n"
                                             f"Budget: ${budget_amount:.2f}\nSpent: ${total_spent:.2f}\n"
                                             f"Remaining: ${remaining:.2f}")

    
# Function to load expenses
def load_expenses():
    """Loads all expenses from the database into the TreeView."""
    try:
        for row in tree.get_children():
            tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT date, time, category, amount, description FROM expenses")
        expenses = cursor.fetchall()
        conn.close()

        # Insert fetched data into TreeView
        for expense in expenses:
            tree.insert("", "end", values=expense)

        messagebox.showinfo("Success", "Expenses loaded successfully!")

    except tk.TclError:
        # Window was closed while trying to update the UI — safe to ignore
        pass

    except Exception as e:
        try:
            messagebox.showerror("Database Error", f"An error occurred while loading expenses: {e}")
        except tk.TclError:
            pass



def show_chart():
    """Displays a pie chart of expenses grouped by category."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()
        conn.close()

        if not data:
            try:
                messagebox.showerror("No Data", "No expense data available to display a chart.")
            except tk.TclError:
                pass
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        # Create and show the chart
        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140,
               colors=["#3498DB", "#2ECC71", "#F39C12", "#E74C3C", "#9B59B6"])
        ax.set_title("Expense Distribution")

        try:
            chart_window = tk.Toplevel(root)
            chart_window.title("Expense Chart")
            chart_window.geometry("500x500")

            canvas = FigureCanvasTkAgg(fig, master=chart_window)
            canvas.get_tk_widget().pack()
            canvas.draw()
        except tk.TclError:
            pass

    except Exception as e:
        try:
            messagebox.showerror("Chart Error", f"An error occurred while generating the chart: {e}")
        except tk.TclError:
            pass



def clear_fields():
    """Clears all input fields in the UI safely."""
    try:
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        category_dropdown.set("")  # Resets category selection
    except tk.TclError:
        pass  # GUI has been closed — ignore safely


def export_to_csv():
    """Exports all expense data to a CSV file."""
    print("🔹 Exporting data to CSV...")  # Debugging

    try:
        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            print("⚠️ No file path selected, export cancelled.")
            return

        # Connect to database and fetch all expenses
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT date, time, category, amount, description FROM expenses")
        expenses = cursor.fetchall()
        conn.close()

        if not expenses:
            try:
                messagebox.showerror("Error", "No expenses found in the database!")
            except tk.TclError:
                pass
            print("⚠️ No expenses found in the database.")
            return

        # Use pandas to structure and export
        df = pd.DataFrame(expenses, columns=["Date", "Time", "Category", "Amount", "Description"])
        df.to_csv(file_path, index=False)

        try:
            messagebox.showinfo("Export Successful", f"Expenses exported successfully to:\n{file_path}")
        except tk.TclError:
            pass

        print(f"✅ Exported to {file_path}")

    except tk.TclError:
        # User closed the app while dialog/messagebox was open
        print("⚠️ App was closed during export operation.")

    except Exception as e:
        try:
            messagebox.showerror("Export Error", f"An error occurred: {e}")
        except tk.TclError:
            pass
        print(f"❌ Export failed: {e}")


# GUI setup
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("800x600")
root.configure(bg="#2C3E50")  # Dark background

# Use pack once to define a main frame
main_frame = tk.Frame(root, bg="#2C3E50")
main_frame.pack(fill="both", expand=True)

# Style for widgets
style = ttk.Style()
style.theme_use("default")  # ✅ This line is essential on Windows

style.configure("Primary.TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"))
style.configure("Danger.TButton", background="#e74c3c", foreground="white", font=("Arial", 10, "bold"))
style.configure("Secondary.TButton", background="#95a5a6", foreground="white", font=("Arial", 10, "bold"))
style.configure("Highlight.TButton", background="#2ecc71", foreground="white", font=("Arial", 10, "bold"))
style.configure("Visual.TButton", background="#9b59b6", foreground="white", font=("Arial", 10, "bold"))

# Ensure button colors are applied even on hover and active states
style.map("Primary.TButton",
          background=[("active", "#2980b9")],
          foreground=[("active", "white")])
style.map("Secondary.TButton",
          background=[("active", "#7f8c8d")],
          foreground=[("active", "white")])
style.map("Danger.TButton",
          background=[("active", "#c0392b")],
          foreground=[("active", "white")])


style.configure("TButton",
                font=("Arial", 10, "bold"),
                padding=10,
                borderwidth=1,
                relief="flat",
                background="#F1C40F",  # Golden Yellow
                foreground="black")

style.configure("TLabel",
                background="#2C3E50",
                foreground="white",
                font=("Arial", 10, "bold"))

# Entry field background
entry_bg = "#ECF0F1"  # Light Grey

# Labels and entries using grid in main_frame
tk.Label(main_frame, text="Amount", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
amount_entry = tk.Entry(main_frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


# Category
tk.Label(main_frame, text="Category", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(main_frame, textvariable=category_var, values=["Food", "Transport", "Bills", "Entertainment", "Others"])
category_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

tk.Label(main_frame, text="Description", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
description_entry = tk.Entry(main_frame)
description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


# Row 3: Action buttons (clearly visible, own row)
tk.Button(main_frame, text="Add Expense", command=add_expense,
          bg="#3498db", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=10)

tk.Button(main_frame, text="Clear", command=clear_fields,
          bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=1, padx=5, pady=10)

tk.Button(main_frame, text="Delete", command=delete_expense,
          bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=2, padx=5, pady=10)


# Action buttons
ttk.Button(main_frame, text="Add Expense", command=add_expense, style="Primary.TButton").grid(row=3, column=0, padx=5, pady=10)
ttk.Button(main_frame, text="Clear", command=clear_fields, style="Secondary.TButton").grid(row=3, column=1, padx=5, pady=10)

# Optional: Delete button if needed
# ttk.Button(main_frame, text="Delete", command=delete_expense, style="Danger.TButton").grid(row=3, column=2, padx=5, pady=10)

# Make column 1 expand to fill space
main_frame.columnconfigure(1, weight=1)


# Expense TreeView
tree = ttk.Treeview(main_frame, columns=("Date", "Time", "Category", "Amount", "Description"), show="headings")
tree.heading("Date", text="Date")
tree.heading("Time", text="Time")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Optional: Let the table expand with window size
main_frame.rowconfigure(4, weight=1)
main_frame.columnconfigure(0, weight=1)

# More buttons inside main_frame
tk.Button(main_frame, text="Load Expenses", command=load_expenses, bg="#27AE60", fg="white", font=("Arial", 10, "bold")).grid(row=5, column=0, padx=8, pady=8)
tk.Button(main_frame, text="Show Chart", command=show_chart, bg="#8E44AD", fg="white", font=("Arial", 10, "bold")).grid(row=5, column=1, padx=8, pady=8)


# Extra buttons inside main_frame
tk.Button(main_frame, text="Check Budget", command=check_budget, bg="#3498DB", fg="white", font=("Arial", 10, "bold")).grid(row=6, column=2, padx=8, pady=8)
tk.Button(main_frame, text="Check Daily Expenses", command=calculate_daily_expenses, bg="#FFA500", fg="black", font=("Arial", 10, "bold")).grid(row=7, column=0, padx=8, pady=8)
tk.Button(main_frame, text="Export to CSV", command=export_to_csv, bg="#16A085", fg="white", font=("Arial", 10, "bold")).grid(row=7, column=1, padx=8, pady=8)



# Section to input monthly budget inside main_frame
# Budget label and entry — place this with the rest of your input fields
# Budget input section (place this where other widgets like Entry and Label are defined)
tk.Label(main_frame, text="Enter Monthly Budget", bg="#2C3E50", fg="white", font=("Arial", 10, "bold")).grid(row=8, column=0, padx=8, pady=8, sticky="w")

global monthly_budget_entry
monthly_budget_entry = ttk.Entry(main_frame)
monthly_budget_entry.grid(row=8, column=1, padx=8, pady=8, sticky="ew")




tk.Button(main_frame, text="Save Budget", command=check_budget, bg="#3498DB", fg="white", font=("Arial", 10, "bold")).grid(row=8, column=2, padx=8, pady=8)


load_expenses()

root.mainloop()
