import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("votes", ascending=False).drop_duplicates(subset=["name", "location"])

    # first cuisine listed = main cuisine
    df["primary_cuisine"] = df["cuisines"].str.split(",").str[0].str.strip()

    # group numeric columns into labelled bands
    df["rating_band"] = pd.cut(df["rate"], bins=[0, 3, 3.5, 4, 5],
                               labels=["low", "average", "good", "excellent"]).astype(str)
    df["cost_band"] = pd.cut(df["cost_for_two"], bins=[0, 300, 600, 1000, 10000],
                             labels=["budget", "mid", "premium", "luxury"]).astype(str)

    # Yes/No -> 1/0
    df["online_order"] = df["online_order"].map({"Yes": 1, "No": 0})
    df["book_table"] = df["book_table"].map({"Yes": 1, "No": 0})
    return df