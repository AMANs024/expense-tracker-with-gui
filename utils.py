import pandas as pd
import os

EXPENSE_FILE = "expenses.csv"

def init_expense_file():
    if not os.path.exists(EXPENSE_FILE):
        pd.DataFrame(columns=["Date", "Amount", "Category"]).to_csv(EXPENSE_FILE, index=False)

def add_expense_to_csv(date, amount, category):
    expense = pd.DataFrame([[date, amount, category]], columns=["Date", "Amount", "Category"])
    expense.to_csv(EXPENSE_FILE, mode='a', header=False, index=False)

def get_filtered_expenses(month=None, category=None):
    data = pd.read_csv(EXPENSE_FILE)
    if month:
        data = data[data['Date'].str.startswith(month)]
    if category:
        data = data[data['Category'] == category]
    return data