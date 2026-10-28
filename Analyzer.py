import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class RetailAnalyzer:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        if not os.path.exists(file_path):
            print("File not found. Check the path and try again.")
            return False

        if not file_path.lower().endswith(".csv"):
            print("Please use a CSV file.")
            return False

        try:
            data = pd.read_csv(file_path)
            data.columns = data.columns.str.strip()

            required = [
                "Date", "Product", "Category",
                "Price", "Quantity Sold", "Total Sales"
            ]

            for column in required:
                if column not in data.columns:
                    print("Required column is missing:", column)
                    return False

            data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
            for column in ["Price", "Quantity Sold", "Total Sales"]:
                data[column] = pd.to_numeric(data[column], errors="coerce")

            data["Product"] = data["Product"].astype("string").str.strip()
            data["Category"] = data["Category"].astype("string").str.strip()

            data.replace({"Product": {"": pd.NA}, "Category": {"": pd.NA}}, inplace=True)
            data.dropna(
                subset=["Date", "Product", "Category", "Price", "Quantity Sold"],
                inplace=True
            )

            data = data[
                (data["Price"] >= 0) &
                (data["Quantity Sold"] > 0)
            ].copy()

            # Calculate sales again so the value matches price multiplied by quantity.
            data["Total Sales"] = data["Price"] * data["Quantity Sold"]

            if data.empty:
                print("No valid sales rows were found.")
                return False

            self.data = data
            print("Dataset loaded successfully.")
            print("Valid rows:", len(self.data))
            return True

        except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
            print("Could not read the CSV file:", error)
            return False

    def calculate_metrics(self):
        if self.data is None or self.data.empty:
            print("Load a dataset first.")
            return

        total_sales = self.data["Total Sales"].sum()
        average_sale = self.data["Total Sales"].mean()
        product_units = self.data.groupby("Product")["Quantity Sold"].sum()
        popular_product = product_units.idxmax()
        sales_values = np.array(self.data["Total Sales"], dtype=float)

        print("\n--- SALES METRICS ---")
        print(f"Total sales: Rs. {total_sales:,.2f}")
        print(f"Average sale per record: Rs. {average_sale:,.2f}")
        print("Most popular product by units sold:", popular_product)
        print(f"Standard deviation: Rs. {np.std(sales_values):,.2f}")

        # This compares the first and last records; it is not a full-period growth rate.
        first_sale = self.data.iloc[0]["Total Sales"]
        last_sale = self.data.iloc[-1]["Total Sales"]
        if first_sale != 0:
            change = (last_sale - first_sale) / first_sale * 100
            print(f"First-to-last record change: {change:.2f}%")
        else:
            print("First-to-last change cannot be calculated because the first sale is zero.")

    def filter_data(self, condition):
        if self.data is None or self.data.empty:
            print("Load a dataset first.")
            return

        if condition == "1":
            value = input("Enter category: ").strip()
            result = self.data[self.data["Category"].str.casefold() == value.casefold()]
        elif condition == "2":
            value = input("Enter product: ").strip()
            result = self.data[self.data["Product"].str.casefold() == value.casefold()]
        elif condition == "3":
            try:
                start = pd.to_datetime(input("Start date (YYYY-MM-DD): "), errors="raise")
                end = pd.to_datetime(input("End date (YYYY-MM-DD): "), errors="raise")
                if start > end:
                    print("Start date must not be after end date.")
                    return
                result = self.data[self.data["Date"].between(start, end)]
            except (ValueError, TypeError):
                print("Please enter valid dates in YYYY-MM-DD format.")
                return
        elif condition == "4":
            try:
                minimum = float(input("Minimum total sale amount: "))
                result = self.data[self.data["Total Sales"] >= minimum]
            except ValueError:
                print("Enter a valid number.")
                return
        else:
            print("Invalid filter option.")
            return

        if result.empty:
            print("No matching records found.")
        else:
            print(result.to_string(index=False))
            print(f"\nFiltered total sales: Rs. {result['Total Sales'].sum():,.2f}")

    def display_summary(self):
        if self.data is None or self.data.empty:
            print("Load a dataset first.")
            return

        print("\n--- DATASET SUMMARY ---")
        print("Number of valid records:", len(self.data))
        print("\nFirst five rows:")
        print(self.data.head().to_string(index=False))
        print("\nMissing values after cleaning:")
        print(self.data.isna().sum().to_string())
        print("\nSales by category:")
        print(self.data.groupby("Category")["Total Sales"].sum().sort_values(ascending=False))
        print("\nSales by product:")
        print(self.data.groupby("Product")["Total Sales"].sum().sort_values(ascending=False))
        print("\nSales by date:")
        print(self.data.groupby("Date")["Total Sales"].sum().sort_index())

    def show_charts(self):
        if self.data is None or self.data.empty:
            print("Load a dataset first.")
            return

        sns.set_theme(style="whitegrid")

        category_sales = self.data.groupby("Category")["Total Sales"].sum().sort_values(ascending=False)
        plt.figure(figsize=(9, 5))
        sns.barplot(x=category_sales.index, y=category_sales.values)
        plt.title("Total Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales (Rs.)")
        plt.xticks(rotation=25)
        plt.tight_layout()
        plt.show()

        daily_sales = self.data.groupby("Date")["Total Sales"].sum().sort_index()
        plt.figure(figsize=(10, 5))
        plt.plot(daily_sales.index, daily_sales.values, marker="o")
        plt.title("Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales (Rs.)")
        plt.xticks(rotation=40)
        plt.tight_layout()
        plt.show()

        correlation = self.data[["Price", "Quantity Sold", "Total Sales"]].corr()
        plt.figure(figsize=(7, 5))
        sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Price, Quantity and Sales Correlation")
        plt.tight_layout()
        plt.show()


def main():
    analyzer = RetailAnalyzer()

    while True:
        print("\n===== RETAIL SALES DATA ANALYZER =====")
        print("1. Load CSV file")
        print("2. Calculate sales metrics")
        print("3. Filter sales data")
        print("4. Display data summary")
        print("5. Show charts")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            path = input("Enter CSV file path: ").strip().strip('"')
            analyzer.load_data(path)
        elif choice == "2":
            analyzer.calculate_metrics()
        elif choice == "3":
            print("\n1. Filter by category")
            print("2. Filter by product")
            print("3. Filter by date range")
            print("4. Filter by minimum sale amount")
            analyzer.filter_data(input("Choose filter (1-4): ").strip())
        elif choice == "4":
            analyzer.display_summary()
        elif choice == "5":
            analyzer.show_charts()
        elif choice == "6":
            print("Thank you for using Retail Sales Data Analyzer.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
