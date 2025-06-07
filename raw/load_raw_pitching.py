import pandas as pd
import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

# Load data file
data = pd.read_csv("raw/pitching.csv")

# Remove column that's entirely null
data = data.drop(columns=["MLBAMID"])

# Rename columns to fit table declaration
data.columns = ["name", "team", "age", "ip", "k_per_nine", "bb_per_nine", "k_per_bb", "hr_per_nine", "k_rate", "bb_rate", "k_minus_bb_rate", "avg", "whip", "babip", "lob_rate", "era", "fip", "e_minus_f", "alt_name", "id"]

data.to_sql("raw_pitching", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'raw_pitching' replaced with new data. {len(data)} records added.")