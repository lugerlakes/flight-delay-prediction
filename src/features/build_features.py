import pandas as pd
import numpy as np

def is_high_season(fecha: pd.Timestamp) -> int:
    """
    Determine if a date falls within high season ranges.
    
    Ranges defined (based on V1 logic):
    - Dec 15 - Mar 3
    - Jul 15 - Jul 31
    - Sep 11 - Sep 30
    - Dec 15 - Jan 3 
    
    Parameters
    ----------
    fecha : pd.Timestamp
        The scheduled departure date.

    Returns
    -------
    int : 1 if high season, 0 otherwise.
    """
    if pd.isnull(fecha):
        return 0
        
    ranges = [
        (pd.Timestamp('2016-12-15'), pd.Timestamp('2017-03-03')),
        (pd.Timestamp('2017-07-15'), pd.Timestamp('2017-07-31')),
        (pd.Timestamp('2017-09-11'), pd.Timestamp('2017-09-30')),
        (pd.Timestamp('2017-12-15'), pd.Timestamp('2018-01-03'))
    ]

    for start, end in ranges:
        if start <= fecha <= end:
            return 1
    return 0

def get_period_day(fecha: pd.Timestamp) -> str:
    """
    Classifies the time of day based on scheduled departure hour.
    
    Logic:
    - Morning: 05:00 - 11:59
    - Afternoon: 12:00 - 18:59
    - Night: 19:00 - 04:59

    Parameters
    ----------
    fecha : pd.Timestamp

    Returns
    -------
    str : 'morning', 'afternoon', or 'night'
    """
    if pd.isnull(fecha):
        return "unknown"
    
    hour = fecha.hour
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 19:
        return "afternoon"
    else:
        return "night"

def build_synthetic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orchestrates the creation of synthetic features and the target variable.

    Features created:
    - min_diff (float): Difference in minutes between actual and scheduled departure.
    - delay_15 (int): Target variable (1 if min_diff > 15).
    - high_season (int): 1 if date is in high season.
    - period_day (str): Time of day segment.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed dataframe with English headers.

    Returns
    -------
    pd.DataFrame
        Dataframe with new features.
    """

    df = df.copy()

    required_cols = ['actual_departure', 'scheduled_departure']
    if not all(col in df.columns for col in required_cols):
        raise KeyError(f"Missing required columns. Expected English names: {required_cols}")

    # 1. Target Construction
    # Calculation: Actual - Scheduled
    df['min_diff'] = (df['actual_departure'] - df['scheduled_departure']).dt.total_seconds() / 60
    df['delay_15'] = np.where(df['min_diff'] > 15, 1, 0)
    
    # 2. Synthetic Features (Seasonality & Time)
    df['high_season'] = df['scheduled_departure'].apply(is_high_season)
    df['period_day'] = df['scheduled_departure'].apply(get_period_day)
    
    return df

def export_features(df: pd.DataFrame, path: str = "data/processed/synthetic_features.csv"):
    """
    Save DataFrame with synthetic features to CSV.
    """
    try:
        df.to_csv(path, index=False)
        print(f"✅ Synthetic features exported successfully to: {path}")
    except Exception as e:
        print(f"❌ Error exporting features: {e}")