import pandas as pd
import numpy as np
from datetime import datetime

def is_high_season(fecha: pd.Timestamp) -> int:
    """
    Determine if the date falls within high season.

    Parameters
    ----------
    fecha : pd.Timestamp

    Returns
    -------
    int : 1 if high season, 0 otherwise
    """
    if pd.isnull(fecha):
        return 0
    
    year = fecha.year
    ranges = [
        (f"{year}-12-15", f"{year + 1}-03-03"),
        (f"{year}-07-15", f"{year}-07-31"),
        (f"{year}-09-11", f"{year}-09-30"),
    ]
    
    for start, end in ranges:
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
