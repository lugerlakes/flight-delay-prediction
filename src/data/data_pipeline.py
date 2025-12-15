import pandas as pd
import numpy as np
from .load_data import load_raw_data
from .preprocess import sanitize_columns, parse_dates

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates the target variable and basic time-based features.
    Assumes input columns are already in English and parsed as datetimes.
    """
    df = df.copy()
    
    # 1. Target Construction: delay_15
    # Logic: Difference in minutes between actual and scheduled departure
    if 'actual_departure' in df.columns and 'scheduled_departure' in df.columns:
        df['min_diff'] = (df['actual_departure'] - df['scheduled_departure']).dt.total_seconds() / 60
        df['delay_15'] = np.where(df['min_diff'] > 15, 1, 0)
    
    # 2. Time Features (Seasonality & Opera Context)
    if 'scheduled_departure' in df.columns:
        # Extract basic components
        df['month'] = df['scheduled_departure'].dt.month
        df['day_of_week'] = df['scheduled_departure'].dt.day_of_week # 0=Monday
        df['hour_scheduled'] = df['scheduled_departure'].dt.hour
        
        # Period of Day (Morning, Afternoon, Night)
        def get_period(hour):
            if 5 <= hour <= 11: return 'morning'
            elif 12 <= hour <= 18: return 'afternoon'
            else: return 'night'
            
        df['period_day'] = df['hour_scheduled'].apply(get_period)
    
    return df

def run_pipeline(filepath: str = "data/raw/civil_aviation_delay_data.csv") -> pd.DataFrame:
    """
    Orchestrates the pipeline: Load -> Sanitize -> Type Cast -> Feature Eng.
    """
    # 1. Load Data 
    df_raw = load_raw_data(filepath)
    
    # 2. Standardization 
    df_clean = sanitize_columns(df_raw)
    
    # 3. Type Casting (Strings -> Datetime)
    df_parsed = parse_dates(df_clean)
    
    # 4. Feature Engineering (Target creation)
    df_final = feature_engineering(df_parsed)
    
    return df_final