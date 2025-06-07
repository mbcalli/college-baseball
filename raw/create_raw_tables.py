import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

with open("raw/create_raw_batting.sql", "r") as file:
    create_raw_batting_sql = file.read()

cursor.executescript(create_raw_batting_sql)
print("Table 'raw_batting' created in 'baseball.db'")

with open("raw/create_raw_pitching.sql", "r") as file:
    create_raw_pitching_sql = file.read()

cursor.executescript(create_raw_pitching_sql)
print("Table 'raw_pitching' created in 'baseball.db'")

connection.commit()
connection.close()

