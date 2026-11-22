import logging
import pandas as pd

log = logging.getLogger(__name__)

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "approx_cost(for two people)": "cost_for_two",
        "listed_in(type)": "service_type",
        "listed_in(city)": "city",
    })

    n = len(df)
    df = df.drop_duplicates()
    log.info("rule 1 duplicates removed: %d", n - len(df))

    # "4.1/5" -> 4.1 ; "NEW" and "-" cannot be converted, so they become NaN
    df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False).str.strip()
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    # "1,200" -> 1200
    df["cost_for_two"] = pd.to_numeric(
        df["cost_for_two"].astype(str).str.replace(",", "", regex=False),
        errors="coerce")

    n = len(df)
    df = df.dropna(subset=["rate"])
    log.info("rule 2 rows without a valid rating removed: %d", n - len(df))

    n = len(df)
    df = df.dropna(subset=["cost_for_two", "location", "cuisines"])
    log.info("rule 3 rows missing cost/location/cuisine removed: %d", n - len(df))

    return df