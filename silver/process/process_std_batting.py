import pandas as pd
import numpy as np
import sqlite3

connection = sqlite3.connect("baseball.db")

data = pd.read_sql("SELECT * FROM bronze_std_batting", connection)

## Percentiles
columns_to_percentile = [
    "g",
    "ab",
    "pa",
    "h",
    "1b",
    "2b",
    "3b",
    "hr",
    "r",
    "rbi",
    "bb",
    "so",
    "hbp",
    "sf",
    "sh",
    "gdp",
    "sb",
    "cs",
    "avg",
]

lower_is_better = [
    "so", "gdp", "cs"
]

percentile_columns = [f"{column}_percentile" for column in columns_to_percentile]

for column_to_percentile, percentile_column in zip(columns_to_percentile, percentile_columns):
    if column_to_percentile in lower_is_better:
        k = -1
    else:
        k = 1
    data[percentile_column] = (k * data[column_to_percentile]).rank(pct=True)
    data[percentile_column] = 100 * data[percentile_column]
    data[percentile_column] = data[percentile_column].astype(int)

data = data[["id", "name", "team"] + percentile_columns]

data.to_sql("silver_std_batting", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'silver_std_batting' replaced with new data. {len(data)} records added.")