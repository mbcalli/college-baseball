import sqlite3

connection = sqlite3.connect("baseball.db")

cursor = connection.cursor()

with open("bronze/tables/bronze_adv_batting.sql", "r") as file:
    create_bronze_adv_batting_sql = file.read()

cursor.executescript(create_bronze_adv_batting_sql)
print("Table 'bronze_adv_batting' created in 'baseball.db'")

with open("bronze/tables/bronze_adv_pitching.sql", "r") as file:
    create_bronze_adv_pitching_sql = file.read()

cursor.executescript(create_bronze_adv_pitching_sql)
print("Table 'bronze_adv_pitching' created in 'baseball.db'")

with open("bronze/tables/bronze_std_batting.sql", "r") as file:
    create_bronze_std_batting_sql = file.read()

cursor.executescript(create_bronze_std_batting_sql)
print("Table 'bronze_std_batting' created in 'baseball.db'")

with open("bronze/tables/bronze_std_pitching.sql", "r") as file:
    create_bronze_std_pitching_sql = file.read()

cursor.executescript(create_bronze_std_pitching_sql)
print("Table 'bronze_std_pitching' created in 'baseball.db'")

connection.commit()
connection.close()

