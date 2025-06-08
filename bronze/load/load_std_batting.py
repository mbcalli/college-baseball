import pandas as pd
import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

# Load data file
data = pd.read_csv("bronze/data/std_batting.csv")

# Remove column that's entirely null
data = data.drop(columns=["MLBAMID"])

# Rename columns to fit table declaration
data.columns = ["name", "team", "age", "g", "ab", "pa", "h", "1b", "2b", "3b", "hr", "r", "rbi", "bb", "so", "hbp", "sf", "sh", "gdp", "sb", "cs", "avg", "alt_name", "id"]

data.to_sql("bronze_std_batting", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'bronze_std_batting' replaced with new data. {len(data)} records added.")