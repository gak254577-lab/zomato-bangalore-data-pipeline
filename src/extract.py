import pandas as pd

COLUMNS = ["name", "online_order", "book_table", "rate", "votes", "location",
           "rest_type", "cuisines", "approx_cost(for two people)",
           "listed_in(type)", "listed_in(city)"]

def extract(path: str = "data/raw/zomato.csv") -> pd.DataFrame:
    return pd.read_csv(path, usecols=COLUMNS)