import sqlite3
import pandas as pd
from src.clean import clean
from src.transform import transform
from src.load import load

def make_row(**kw):
    row = {"name": "A", "online_order": "Yes", "book_table": "No",
           "rate": "4.0/5", "votes": 10, "location": "BTM",
           "rest_type": "Cafe", "cuisines": "Cafe, Italian",
           "approx_cost(for two people)": "500",
           "listed_in(type)": "Delivery", "listed_in(city)": "BTM"}
    row.update(kw)
    return row

def test_clean_parses_rate_and_cost():
    df = pd.DataFrame([
        make_row(name="a", rate="4.1/5", **{"approx_cost(for two people)": "1,200"}),
        make_row(name="b", rate="3.9 /5"),
        make_row(name="c", rate="NEW"),
        make_row(name="d", rate="-"),
    ])
    out = clean(df)
    assert sorted(out["rate"].tolist()) == [3.9, 4.1]
    assert out.loc[out["name"] == "a", "cost_for_two"].iloc[0] == 1200

def test_clean_removes_exact_duplicates():
    df = pd.DataFrame([make_row(), make_row()])
    assert len(clean(df)) == 1

def test_transform_keeps_highest_votes_per_restaurant():
    df = clean(pd.DataFrame([
        make_row(name="X", votes=5),
        make_row(name="X", votes=50, **{"listed_in(type)": "Dine-out"}),
    ]))
    out = transform(df)
    assert len(out) == 1
    assert out["votes"].iloc[0] == 50

def test_load_is_idempotent(tmp_path):
    db = str(tmp_path / "test.db")
    df = pd.DataFrame({"a": [1, 2, 3]})
    load(df, db)
    load(df, db)
    conn = sqlite3.connect(db)
    count = conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
    conn.close()
    assert count == 3