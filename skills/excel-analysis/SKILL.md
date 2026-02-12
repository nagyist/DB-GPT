---
name: Excel Analysis
description: Analyze Excel spreadsheets, create pivot tables, generate charts, and perform data analysis. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
config:
  scripts:
    - name: load_and_preview
      description: Load Excel file and display basic info plus first 5 rows
      language: python
      code: |
        import pandas as pd
        import json

        file_path = r"${file_path}"
        df = pd.read_excel(file_path)

        result = {
            "shape": df.shape,
            "columns": list(df.columns),
            "head": df.head(5).to_dict(orient="records")
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    - name: column_statistics
      description: Calculate descriptive statistics for a specific column
      language: python
      code: |
        import pandas as pd
        import json

        file_path = r"${file_path}"
        column_name = "${column_name}"

        df = pd.read_excel(file_path)

        if column_name in df.columns:
            stats = df[column_name].describe()
            print(f"Statistics for column '{column_name}':")
            print(json.dumps(stats.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(f"Error: Column '{column_name}' not found. Available columns: {list(df.columns)}")

    - name: groupby_analysis
      description: Group by a column and calculate aggregations
      language: python
      code: |
        import pandas as pd
        import json

        file_path = r"${file_path}"
        group_column = "${group_column}"
        agg_column = "${agg_column}"
        agg_func = "${agg_func}"

        df = pd.read_excel(file_path)

        if group_column not in df.columns:
            print(f"Error: Group column '{group_column}' not found.")
        elif agg_column not in df.columns:
            print(f"Error: Aggregate column '{agg_column}' not found.")
        else:
            result = df.groupby(group_column)[agg_column].agg(agg_func).reset_index()
            print(json.dumps(result.to_dict(orient="records"), ensure_ascii=False, indent=2))

    - name: correlation_matrix
      description: Calculate correlation matrix for numeric columns
      language: python
      code: |
        import pandas as pd
        import json

        file_path = r"${file_path}"
        df = pd.read_excel(file_path)

        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])

        if numeric_df.empty:
            print("No numeric columns found for correlation analysis.")
        else:
            corr = numeric_df.corr()
            print("Correlation matrix:")
            print(json.dumps(corr.to_dict(), ensure_ascii=False, indent=2))

    - name: filter_data
      description: Filter data based on conditions
      language: python
      code: |
        import pandas as pd
        import json

        file_path = r"${file_path}"
        column = "${column}"
        operator = "${operator}"
        value = "${value}"

        df = pd.read_excel(file_path)

        if column not in df.columns:
            print(f"Error: Column '{column}' not found.")
        else:
            # Try to convert value to number if possible
            try:
                value = float(value)
            except:
                pass

            if operator == "eq":
                filtered = df[df[column] == value]
            elif operator == "gt":
                filtered = df[df[column] > value]
            elif operator == "lt":
                filtered = df[df[column] < value]
            elif operator == "ge":
                filtered = df[df[column] >= value]
            elif operator == "le":
                filtered = df[df[column] <= value]
            elif operator == "ne":
                filtered = df[df[column] != value]
            elif operator == "contains":
                filtered = df[df[column].astype(str).str.contains(str(value), na=False)]
            else:
                print(f"Error: Unknown operator '{operator}'")
                filtered = pd.DataFrame()

            print(f"Filtered {len(filtered)} rows out of {len(df)}")
            print(json.dumps(filtered.head(20).to_dict(orient="records"), ensure_ascii=False, indent=2))
---

# Excel Analysis

## Quick start

Read Excel files with pandas:

```python
import pandas as pd

# Read Excel file
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Display first few rows
print(df.head())

# Basic statistics
print(df.describe())
```

## Instructions for Script Usage

This skill provides pre-defined scripts that can be executed using the `execute_skill_script` tool:

1. **load_and_preview**: Load file and show basic statistics
   - Args: `{"file_path": "/path/to/file.xlsx"}`

2. **column_statistics**: Get statistics for a specific column
   - Args: `{"file_path": "...", "column_name": "Sales"}`

3. **groupby_analysis**: Group and aggregate data
   - Args: `{"file_path": "...", "group_column": "Region", "agg_column": "Sales", "agg_func": "sum"}`

4. **correlation_matrix**: Analyze correlations between numeric columns
   - Args: `{"file_path": "..."}`

5. **filter_data**: Filter rows based on conditions
   - Args: `{"file_path": "...", "column": "Sales", "operator": "gt", "value": "1000"}`

Operators: eq, gt, lt, ge, le, ne, contains

## Reading multiple sheets

Process all sheets in a workbook:

```python
import pandas as pd

# Read all sheets
excel_file = pd.ExcelFile("workbook.xlsx")

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"\n{sheet_name}:")
    print(df.head())
```

## Data analysis

Perform common analysis tasks:

```python
import pandas as pd

df = pd.read_excel("sales.xlsx")

# Group by and aggregate
sales_by_region = df.groupby("region")["sales"].sum()
print(sales_by_region)

# Filter data
high_sales = df[df["sales"] > 10000]

# Calculate metrics
df["profit_margin"] = (df["revenue"] - df["cost"]) / df["revenue"]

# Sort by column
df_sorted = df.sort_values("sales", ascending=False)
```

## Creating Excel files

Write data to Excel with formatting:

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150],
    "Profit": [20, 40, 30]
})

# Write to Excel
writer = pd.ExcelWriter("output.xlsx", engine="openpyxl")
df.to_excel(writer, sheet_name="Sales", index=False)

# Get worksheet for formatting
worksheet = writer.sheets["Sales"]

# Auto-adjust column widths
for column in worksheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
    worksheet.column_dimensions[column_letter].width = max_length + 2

writer.close()
```

## Pivot tables

Create pivot tables programmatically:

```python
import pandas as pd

df = pd.read_excel("sales_data.xlsx")

# Create pivot table
pivot = pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

# Save pivot table
pivot.to_excel("pivot_report.xlsx")
```

## Charts and visualization

Generate charts from Excel data:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data.xlsx")

# Create bar chart
df.plot(x="category", y="value", kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("chart.png")

# Create pie chart
df.set_index("category")["value"].plot(kind="pie", autopct="%1.1f%%")
plt.title("Market Share")
plt.ylabel("")
plt.savefig("pie_chart.png")
```

## Data cleaning

Clean and prepare Excel data:

```python
import pandas as pd

df = pd.read_excel("messy_data.xlsx")

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.fillna(0)  # or df.dropna()

# Remove whitespace
df["name"] = df["name"].str.strip()

# Convert data types
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Save cleaned data
df.to_excel("cleaned_data.xlsx", index=False)
```

## Merging and joining

Combine multiple Excel files:

```python
import pandas as pd

# Read multiple files
df1 = pd.read_excel("sales_q1.xlsx")
df2 = pd.read_excel("sales_q2.xlsx")

# Concatenate vertically
combined = pd.concat([df1, df2], ignore_index=True)

# Merge on common column
customers = pd.read_excel("customers.xlsx")
sales = pd.read_excel("sales.xlsx")

merged = pd.merge(sales, customers, on="customer_id", how="left")

merged.to_excel("merged_data.xlsx", index=False)
```

## Advanced formatting

Apply conditional formatting and styles:

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font

# Create Excel file
df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150]
})

df.to_excel("formatted.xlsx", index=False)

# Load workbook for formatting
wb = load_workbook("formatted.xlsx")
ws = wb.active

# Apply conditional formatting
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")

for row in range(2, len(df) + 2):
    cell = ws[f"B{row}"]
    if cell.value < 150:
        cell.fill = red_fill
    else:
        cell.fill = green_fill

# Bold headers
for cell in ws[1]:
    cell.font = Font(bold=True)

wb.save("formatted.xlsx")
```

## Performance tips

- Use `read_excel` with `usecols` to read specific columns only
- Use `chunksize` for very large files
- Consider using `engine='openpyxl'` or `engine='xlrd'` based on file type
- Use `dtype` parameter to specify column types for faster reading

## Available packages

- **pandas** - Data analysis and manipulation (primary)
- **openpyxl** - Excel file creation and formatting
- **xlrd** - Reading older .xls files
- **xlsxwriter** - Advanced Excel writing capabilities
- **matplotlib** - Chart generation
