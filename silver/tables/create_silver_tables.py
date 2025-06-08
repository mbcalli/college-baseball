import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

with open("silver/tables/silver_adv_batting.sql", "r") as file:
    create_silver_adv_batting = file.read()

cursor.executescript(create_silver_adv_batting)
print("Table 'silver_adv_batting' created in 'baseball.db'")

with open("silver/tables/silver_adv_pitching.sql", "r") as file:
    create_silver_adv_pitching = file.read()

cursor.executescript(create_silver_adv_pitching)
print("Table 'silver_adv_pitching' created in 'baseball.db'")

connection.commit()
connection.close()
