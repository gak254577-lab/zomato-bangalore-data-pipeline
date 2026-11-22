import sqlite3
import pandas as pd

def load(df: pd.DataFrame, db: str = "db/pipeline.db", table: str = "restaurants") -> int:
    conn = sqlite3.connect(db)
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()
    return len(df)