import pandas as pd
import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

# Load data file
data = pd.read_csv("bronze/data/std_pitching.csv")

# Remove column that's entirely null
data = data.drop(columns=["MLBAMID"])

# Rename columns to fit table declaration
data.columns = ["name", "team", "age", "w", "l", "era", "g", "gs", "cg", "sho", "sv", "ip", "tbf", "h", "r", "er", "hr", "bb", "hbp", "wp", "bk", "so", "alt_name", "id"]

data.to_sql("bronze_adv_pitching", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'bronze_adv_pitching' replaced with new data. {len(data)} records added.")