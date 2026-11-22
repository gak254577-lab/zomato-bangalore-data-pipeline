import sqlite3
import pandas as pd

conn = sqlite3.connect("db/pipeline.db")
print(pd.read_sql("SELECT COUNT(*) AS rows_in_table FROM restaurants", conn))
print(pd.read_sql("SELECT rating_band, COUNT(*) AS n FROM restaurants GROUP BY rating_band", conn))
conn.close()