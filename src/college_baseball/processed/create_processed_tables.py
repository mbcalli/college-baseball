import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

with open("processed/create_processed_batting.sql", "r") as file:
    create_processed_batting_sql = file.read()

cursor.executescript(create_processed_batting_sql)

connection.commit()
connection.close()

print("Table 'processed_batting' created in 'baseball.db'")