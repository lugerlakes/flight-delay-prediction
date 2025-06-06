import pandas as pd
import numpy as np
from datetime import datetime

def is_high_season(fecha):
    """
    Determine whether a given date falls within Chile's high season travel periods.

    High season is defined as any date within the following ranges:
    - Dec 15, 2016 to Mar 3, 2017  (Summer holidays)
    - Jul 15, 2017 to Jul 31, 2017 (Winter break)
    - Sep 11, 2017 to Sep 30, 2017 (National holidays)
    - Dec 15, 2017 to Jan 3, 2018  (Christmas & New Year)

    Parameters
    ----------
    fecha : datetime
        The departure date to evaluate (typically `fecha_i`).

    Returns
    -------
    int
        1 if the date is in high season, 0 otherwise.
    """
    import pandas as pd

    high_season_ranges = [
        ("2016-12-15", "2017-03-03"),
        ("2017-07-15", "2017-07-31"),
        ("2017-09-11", "2017-09-30"),
        ("2017-12-15", "2018-01-03"),
    ]

    for start, end in high_season_ranges:
        if pd.to_datetime(start) <= fecha <= pd.to_datetime(end):
            return 1
    return 0



def get_period_day(fecha: pd.Timestamp) -> str:
    """
    Classify time of day.

    Parameters
    ----------
    fecha : pd.Timestamp

    Returns
    -------
    str : "morning", "afternoon", or "night"
    """
    if pd.isnull(fecha):
        return np.nan
    
    hour = fecha.hour
    if 5 <= hour <= 11:
        return "morning"
    elif 12 <= hour <= 18:
        return "afternoon"
    else:
        return "night"

def build_synthetic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add synthetic features to the dataset.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()
    
    df["min_diff"] = (df["fecha_o"] - df["fecha_i"]).dt.total_seconds() / 60
    df["delay_15"] = (df["min_diff"] > 15).astype(int)
    df["high_season"] = df["fecha_i"].apply(is_high_season)
    df["period_day"] = df["fecha_i"].apply(get_period_day)
    
    return df

def export_features(df: pd.DataFrame, path: str = "data/processed/synthetic_features.csv"):
    """
    Save DataFrame with synthetic features to CSV.

    Parameters
    ----------
    df : pd.DataFrame
    path : str
    """
    df.to_csv(path, index=False)
    print(f"✅ Synthetic features exported to: {path}")
