import pandas as pd
import numpy as np
import sqlite3

connection = sqlite3.connect("baseball.db")

data = pd.read_sql("SELECT * FROM bronze_adv_pitching", connection)

## Percentiles
columns_to_percentile = [
    "ip",
    "k_per_nine",
    "bb_per_nine",
    "k_per_bb",
    "hr_per_nine",
    "k_rate",
    "bb_rate",
    "k_minus_bb_rate",
    "avg",
    "whip",
    "babip",
    "lob_rate",
    "era",
    "fip",
    "e_minus_f"
]

lower_is_better = [
    "bb_per_nine",
    "hr_per_nine",
    "bb_rate",
    "avg",
    "whip",
    "babip",
    "era",
    "fip",
    "e_minus_f"
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

data.to_sql("silver_adv_pitching", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'silver_adv_pitching' replaced with new data. {len(data)} records added.")