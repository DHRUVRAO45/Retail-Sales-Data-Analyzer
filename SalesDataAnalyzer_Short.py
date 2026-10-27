import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SalesDataAnalyzer:
    def __init__(self):
        self.data = None
        self.fig = None

    def load_data(self):
        file = input("Enter CSV file path: ")
        try:
            self.data = pd.read_csv(file)
            print("Dataset loaded successfully!")
        except Exception as e:
            print("Error:", e)

    def explore_data(self):
        if self.data is None:
            print("Load a dataset first.")
            return
        print("1. First 5 rows  2. Last 5 rows  3. Columns")
        print("4. Data types   5. Dataset info")
        choice = input("Choose: ")
        if choice == "1":
            print(self.data.head())
        elif choice == "2":
            print(self.data.tail())
        elif choice == "3":
            print(self.data.columns.tolist())
        elif choice == "4":
            print(self.data.dtypes)
        elif choice == "5":
            self.data.info()
            print(self.data.describe(include="all"))
        else:
            print("Invalid choice.")

    def dataframe_operations(self):
        if self.data is None:
            print("Load a dataset first.")
            return
        print("Columns:", self.data.columns.tolist())
        print("1. Sort  2. Filter  3. Group and sum")
        print("4. Split by column  5. Combine CSV  6. NumPy operations")
        choice = input("Choose: ")

        if choice == "1":
            col = input("Sort by column: ")
            if col in self.data.columns:
                print(self.data.sort_values(col))
            else:
                print("Column not found.")
        elif choice == "2":
            col = input("Filter column: ")
            if col in self.data.columns:
                value = input("Value to search: ")
                print(self.data[self.data[col].astype(str).str.contains(
                    value, case=False, na=False)])
            else:
                print("Column not found.")
        elif choice == "3":
            group = input("Group by column: ")
            col = input("Column to add: ")
            if group in self.data.columns and col in self.data.columns:
                print(self.data.groupby(group)[col].sum())
            else:
                print("Column not found.")
        elif choice == "4":
            col = input("Split by column: ")
            if col in self.data.columns:
                for name, part in self.data.groupby(col):
                    print("\n", name)
                    print(part)
            else:
                print("Column not found.")
        elif choice == "5":
            try:
                other = pd.read_csv(input("Second CSV path: "))
                print(pd.concat([self.data, other], ignore_index=True))
            except Exception as e:
                print("Error:", e)
        elif choice == "6":
            arr = self.data.select_dtypes(include=np.number).to_numpy()
            if arr.size:
                print("Array:\n", arr)
                print("Array + 10:\n", arr + 10)
                print("Column sums:", np.sum(arr, axis=0))
            else:
                print("No numeric columns found.")
        else:
            print("Invalid choice.")

    def missing_data(self):
        if self.data is None:
            print("Load a dataset first.")
            return
        print("1. Show missing rows  2. Fill numeric gaps with mean")
        print("3. Drop missing rows  4. Replace gaps with a value")
        choice = input("Choose: ")
        if choice == "1":
            rows = self.data[self.data.isnull().any(axis=1)]
            print(rows if not rows.empty else "No missing values found.")
        elif choice == "2":
            cols = self.data.select_dtypes(include=np.number).columns
            self.data[cols] = self.data[cols].fillna(self.data[cols].mean())
            print("Missing numeric values filled.")
        elif choice == "3":
            self.data.dropna(inplace=True)
            print("Rows with missing values removed.")
        elif choice == "4":
            value = input("Replacement value: ")
            self.data.fillna(value, inplace=True)
            print("Missing values replaced.")
        else:
            print("Invalid choice.")

    def statistics(self):
        if self.data is None:
            print("Load a dataset first.")
            return
        print(self.data.describe(include="all"))
        nums = self.data.select_dtypes(include=np.number)
        if not nums.empty:
            print("\nMean:\n", nums.mean())
            print("\nMedian:\n", nums.median())
            print("\nStandard deviation:\n", nums.std())
            print("\nVariance:\n", nums.var())
            print("\nQuantiles:\n", nums.quantile([.25, .5, .75]))

    def visualize_data(self):
        if self.data is None:
            print("Load a dataset first.")
            return
        print("1. Bar  2. Line  3. Scatter  4. Pie")
        print("5. Histogram  6. Stack  7. Heatmap  8. Box plot")
        choice = input("Choose plot: ")
        nums = self.data.select_dtypes(include=np.number)

        if choice == "1":
            col = input("Column: ")
            if col not in self.data.columns:
                print("Column not found.")
                return
            self.data[col].head(15).plot(kind="bar", title=col)
        elif choice == "2":
            col = input("Numeric column: ")
            if col not in nums.columns:
                print("Numeric column not found.")
                return
            self.data[col].plot(kind="line", marker="o", title=col)
        elif choice == "3":
            x = input("X-axis numeric column: ")
            y = input("Y-axis numeric column: ")
            if x not in nums.columns or y not in nums.columns:
                print("Column not found or not numeric.")
                return
            plt.scatter(self.data[x], self.data[y])
            plt.xlabel(x)
            plt.ylabel(y)
            plt.title(x + " vs " + y)
        elif choice == "4":
            col = input("Category column: ")
            if col not in self.data.columns:
                print("Column not found.")
                return
            self.data[col].value_counts().head(10).plot(
                kind="pie", autopct="%1.1f%%", title=col)
            plt.ylabel("")
        elif choice == "5":
            col = input("Numeric column: ")
            if col not in nums.columns:
                print("Numeric column not found.")
                return
            plt.hist(self.data[col].dropna(), bins=10, edgecolor="black")
            plt.title("Histogram of " + col)
        elif choice == "6":
            cols = list(nums.columns[:4])
            if len(cols) < 2:
                print("Need at least two numeric columns.")
                return
            plt.stackplot(range(len(self.data)),
                          *[self.data[c].fillna(0).to_numpy() for c in cols],
                          labels=cols)
            plt.legend()
            plt.title("Stack Plot")
        elif choice == "7":
            if nums.empty:
                print("No numeric columns found.")
                return
            sns.heatmap(nums.corr(), annot=True, cmap="coolwarm")
            plt.title("Correlation Heatmap")
        elif choice == "8":
            col = input("Numeric column: ")
            if col not in nums.columns:
                print("Numeric column not found.")
                return
            sns.boxplot(x=self.data[col])
            plt.title("Box Plot of " + col)
        else:
            print("Invalid choice.")
            return

        plt.tight_layout()
        self.fig = plt.gcf()
        plt.show()

    def save_plot(self):
        if self.fig is None:
            print("Create a plot first.")
            return
        name = input("File name (e.g. sales_plot.png): ")
        try:
            self.fig.savefig(name)
            print("Plot saved:", name)
        except Exception as e:
            print("Error:", e)


def main():
    app = SalesDataAnalyzer()
    while True:
        print("\n===== Data Analysis & Visualization =====")
        print("1. Load Dataset")
        print("2. Explore Data")
        print("3. DataFrame Operations")
        print("4. Handle Missing Data")
        print("5. Descriptive Statistics")
        print("6. Data Visualization")
        print("7. Save Visualization")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            app.load_data()
        elif choice == "2":
            app.explore_data()
        elif choice == "3":
            app.dataframe_operations()
        elif choice == "4":
            app.missing_data()
        elif choice == "5":
            app.statistics()
        elif choice == "6":
            app.visualize_data()
        elif choice == "7":
            app.save_plot()
        elif choice == "8":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
