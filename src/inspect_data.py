import pandas as pd

df = pd.read_csv("data/raw/zomato.csv", usecols=[
    "name", "online_order", "book_table", "rate", "votes",
    "location", "cuisines", "approx_cost(for two people)"])
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.head())