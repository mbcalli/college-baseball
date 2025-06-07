import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

with open("processed/create_processed_batting.sql", "r") as file:
    create_processed_batting_sql = file.read()

cursor.executescript(create_processed_batting_sql)
print("Table 'processed_batting' created in 'baseball.db'")

with open("processed/create_processed_pitching.sql", "r") as file:
    create_processed_pitching_sql = file.read()

cursor.executescript(create_processed_pitching_sql)
print("Table 'processed_pitching' created in 'baseball.db'")

connection.commit()
connection.close()
