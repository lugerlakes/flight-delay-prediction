# Data Loading and Target Creation

import pandas as pd
import os

def load_raw_data(filepath: str) -> pd.DataFrame:
    """Loads raw data from a specified CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data not found at: {filepath}")
    return pd.read_csv(filepath, parse_dates=['Fecha-I', 'Fecha-O'])

def create_target_and_basics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the target variable (delay_15) and basic time features."""
    df.columns = df.columns.str.lower().str.replace('-', '_')
    
    # Target: 1 if delay > 15 mins
    df['min_diff'] = (df['fecha_o'] - df['fecha_i']).dt.total_seconds() / 60
    df['delay_15'] = (df['min_diff'] > 15).astype(int)
    
    # Basic Time Features
    df['month'] = df['fecha_i'].dt.month
    df['day_of_week'] = df['fecha_i'].dt.day_name()
    df['hour'] = df['fecha_i'].dt.hour
    
    # Simple period_day for consistency
    def get_period(hour):
        if 5 <= hour <= 11: return 'morning'
        elif 12 <= hour <= 18: return 'afternoon'
        else: return 'night'
    df['period_day'] = df['hour'].apply(get_period)
    
    return df