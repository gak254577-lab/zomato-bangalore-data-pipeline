# Bangalore Restaurant Analytics Pipeline

An end-to-end data pipeline (Python + SQLite) that cleans Zomato Bangalore
restaurant data and analyses ratings by cuisine, location, price and online ordering.

## Dataset
Zomato Bangalore Restaurants (Kaggle), 51,717 listings. Not included in this
repo because it is 574 MB. Download it and place it at data/raw/zomato.csv.

## Pipeline stages
Extract -> Clean -> Transform -> Load (SQLite) -> Analyze

## Data cleaning
| Rule | Rows removed | Why |
|------|--------------|-----|
| Exact duplicate rows | 108 | Same record twice |
| No valid rating (NEW, -, blank) | 10,019 | A rating cannot be averaged if it does not exist |
| Missing cost, location or cuisine | 253 | Needed for the analysis |

Transform step: listings were deduplicated by name + location, keeping the
listing with the most votes. 41,337 listings became 9,216 unique restaurants.

## Key findings
1. Luxury restaurants rate highest (4.11); budget (3.55) and mid (3.57) are almost identical.
2. Asian (4.09) and American (4.03) are the best-rated cuisines, but each has only about 60 restaurants.
3. Lavelle Road is the best-rated area (4.08), then St. Marks Road and Koramangala 5th Block (3.92).
4. Restaurants with online ordering rate slightly higher (3.66 vs 3.59), a small gap.
5. Whitefield (584), BTM (516) and HSR (509) have the most restaurants.

## Limitations
- Only rated restaurants are included, so new and unrated places are missing.
- Results show correlation, not causation.
- Cost bands (300, 600, 1000) are arbitrary cut-offs.
- Deduplicating by name + location merges chain outlets in the same area.
- Small groups (about 50 restaurants) can swing an average.

## How to run
pip install -r requirements.txt
python main.py
python -m pytest -v

Charts are saved to outputs/charts/.