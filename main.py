import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_transaction(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("✅ Transaction added successfully.")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors='coerce')
        df["amount"] = pd.to_numeric(df["amount"], errors='coerce')

        start = datetime.strptime(start_date, cls.FORMAT)
        end = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start) & (df["date"] <= end)
        filtered = df.loc[mask].dropna()

        if filtered.empty:
            print("⚠️ No transactions found in the specified date range.")
        else:
            print(f"\n📅 Transactions from {start.strftime(cls.FORMAT)} to {end.strftime(cls.FORMAT)}")
            print(filtered.to_string(index=False, formatters={'date': lambda x: x.strftime(cls.FORMAT)}))

            income = filtered[filtered["category"] == "Income"]["amount"].sum()
            expense = filtered[filtered["category"] == "Expense"]["amount"].sum()
            print("\n📊 Summary:")
            print(f"Total Income: ₹{income:.2f}")
            print(f"Total Expense: ₹{expense:.2f}")
            print(f"Net Savings: ₹{income - expense:.2f}")

        return filtered


def add():
    CSV.initialize_csv()
    date = get_date("Enter date (dd-mm-yyyy): ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_transaction(date, amount, category, description)


def plot_transactions(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df.set_index("date", inplace=True)

    income = df[df["category"] == "Income"].resample("D").sum(numeric_only=True)
    expense = df[df["category"] == "Expense"].resample("D").sum(numeric_only=True)

    plt.figure(figsize=(10, 5))
    plt.plot(income.index, income["amount"], label="Income", color="green")
    plt.plot(expense.index, expense["amount"], label="Expense", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount (₹)")
    plt.title("📈 Daily Income and Expense")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    CSV.initialize_csv()
    while True:
        print("\n📌 Personal Finance Tracker")
        print("1. ➕ Add Transaction")
        print("2. 📄 View Transactions")
        print("3. ❌ Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add()
        elif choice == '2':
            start = get_date("Enter start date (dd-mm-yyyy): ")
            end = get_date("Enter end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start, end)
            if not df.empty and input("Plot the transactions? (y/n): ").lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print("👋 Exiting the application. Stay financially fit!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
