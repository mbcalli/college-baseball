import pandas as pd
import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

# Load data file
data = pd.read_csv("bronze/data/adv_batting.csv")

# Remove column that's entirely null
data = data.drop(columns=["MLBAMID"])

# Rename columns to fit table declaration
data.columns = ["name", "team", "age", "pa", "bb_rate", "k_rate", "bb_per_k", "avg", "obp", "slg", "ops", "iso", "spd", "babip", "wsb", "wrc", "wraa", "woba", "wrc_plus", "alt_name", "id"]

data.to_sql("bronze_adv_batting", connection, if_exists="replace", index=False)

connection.close()

print(f"Table 'bronze_adv_batting' replaced with new data. {len(data)} records added.")