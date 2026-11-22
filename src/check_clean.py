import sqlite3
import pandas as pd

conn = sqlite3.connect("db/pipeline.db")
df = pd.read_sql("SELECT * FROM restaurants", conn)
print(df["rate"].describe())
print(df["cost_for_two"].describe())
print("locations:", df["location"].nunique())
print("untrimmed locations:", (df["location"] != df["location"].str.strip()).sum())
conn.close()