import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # save charts to files, no pop-up windows
import matplotlib.pyplot as plt


def analyze(db: str = "db/pipeline.db") -> None:
    Path("outputs/charts").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)

    # 1. Best-rated cuisines (only cuisines with 50+ restaurants)
    cuisines = pd.read_sql("""
        SELECT primary_cuisine, ROUND(AVG(rate), 2) AS avg_rate, COUNT(*) AS n
        FROM restaurants
        GROUP BY primary_cuisine
        HAVING n >= 50
        ORDER BY avg_rate DESC
        LIMIT 10""", conn)
    cuisines.sort_values("avg_rate").plot.barh(x="primary_cuisine", y="avg_rate", legend=False)
    plt.title("Top 10 cuisines by average rating (50+ restaurants)")
    plt.xlabel("Average rating")
    plt.tight_layout(); plt.savefig("outputs/charts/top_cuisines.png"); plt.close()

    # 2. Best-rated locations (only locations with 30+ restaurants)
    loc = pd.read_sql("""
        SELECT location, ROUND(AVG(rate), 2) AS avg_rate, COUNT(*) AS n
        FROM restaurants
        GROUP BY location
        HAVING n >= 30
        ORDER BY avg_rate DESC
        LIMIT 10""", conn)
    loc.sort_values("avg_rate").plot.barh(x="location", y="avg_rate", legend=False)
    plt.title("Top 10 locations by rating (30+ restaurants)", fontsize=10)
    plt.xlabel("Average rating")
    plt.tight_layout(); plt.savefig("outputs/charts/rating_by_location.png"); plt.close()

    # 3. Does paying more mean a better rating?
    cost = pd.read_sql("""
        SELECT cost_band, ROUND(AVG(rate), 2) AS avg_rate, COUNT(*) AS n
        FROM restaurants
        GROUP BY cost_band
        ORDER BY CASE cost_band WHEN 'budget' THEN 1 WHEN 'mid' THEN 2
                 WHEN 'premium' THEN 3 ELSE 4 END""", conn)
    cost.plot.bar(x="cost_band", y="avg_rate", legend=False, rot=0)
    plt.title("Average rating by cost band")
    plt.ylabel("Average rating")
    plt.tight_layout(); plt.savefig("outputs/charts/rating_by_cost.png"); plt.close()

    # 4. Do restaurants that take online orders rate differently?
    online = pd.read_sql("""
        SELECT CASE online_order WHEN 1 THEN 'Online order' ELSE 'No online order' END AS option,
               ROUND(AVG(rate), 2) AS avg_rate, COUNT(*) AS n
        FROM restaurants GROUP BY online_order""", conn)
    online.plot.bar(x="option", y="avg_rate", legend=False, rot=0)
    plt.title("Average rating: online ordering vs not")
    plt.ylabel("Average rating")
    plt.tight_layout(); plt.savefig("outputs/charts/rating_by_online_order.png"); plt.close()

    # 5. Where are the restaurants?
    locations = pd.read_sql("""
        SELECT location, COUNT(*) AS n
        FROM restaurants GROUP BY location
        ORDER BY n DESC LIMIT 10""", conn)
    locations.sort_values("n").plot.barh(x="location", y="n", legend=False)
    plt.title("Top 10 locations by number of restaurants")
    plt.xlabel("Number of restaurants")
    plt.tight_layout(); plt.savefig("outputs/charts/top_locations.png"); plt.close()

    conn.close()

    for title, table in [("Top cuisines", cuisines),
                         ("Top locations by rating", loc),
                         ("By cost band", cost),
                         ("Online order", online),
                         ("Top locations by count", locations)]:
        print(f"\n{title}\n{table.to_string(index=False)}")