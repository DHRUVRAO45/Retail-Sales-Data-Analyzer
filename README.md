# Retail Sales Data Analyzer

**Author:** Dhruv Rao

## Project overview
This Python project reads a retail sales CSV file, checks and cleans the records, calculates sales metrics, filters records, and displays charts.

## Features
- Checks the CSV file path and required columns.
- Cleans invalid dates, missing key values, prices, and quantities.
- Calculates total sales, average sale per record, popular product by units sold, and standard deviation.
- Filters by category, product, date range, or minimum sale amount.
- Displays a data summary and sales grouped by category, product, and date.
- Creates a category bar chart, daily sales line graph, and correlation heatmap.

## Files
- `retail_analyzer.py` — main Python program.
- `retail_sales.csv` — sample dataset for testing.
- `output.html` — sample results and an HTML summary page.

## Requirements
Python 3.10 or newer is recommended. Install the required libraries in the VS Code terminal:

```bash
python -m pip install pandas numpy matplotlib seaborn
```

## How to run
1. Put `retail_analyzer.py` and `retail_sales.csv` in the same folder.
2. Open that folder in VS Code.
3. Run:

   ```bash
   python retail_analyzer.py
   ```

4. Choose option `1` and enter `retail_sales.csv`.
5. Use the menu to calculate metrics, filter records, view the summary, or show charts.

If the CSV is in another folder, enter its full path. On Windows, paths containing spaces can be entered inside quotes.

## Dataset columns
| Column | Meaning |
|---|---|
| `Date` | Sale date in YYYY-MM-DD format |
| `Product` | Product name |
| `Category` | Product category |
| `Price` | Price per unit |
| `Quantity Sold` | Units sold in the record |
| `Total Sales` | Total sale value |

The program recalculates `Total Sales` as `Price × Quantity Sold` so the totals remain consistent.

## Notes
- The most popular product is selected by the highest total quantity sold.
- The first-to-last percentage compares the first and last records; it is not a full-period growth calculation.
- The heatmap shows correlations between numeric columns. Correlation does not prove causation.
- `output.html` contains sample results calculated from the included sample CSV. Your results will change if you use a different dataset.

## Author
Dhruv Rao
