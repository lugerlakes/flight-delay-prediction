# Feature Engineering Logic

import pandas as pd
import numpy as np

def create_historical_delay_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the historical delay rate for the operator ('opera') and destination ('siglades').
    This is the core operational feature.
    """
    df_temp = df[['opera', 'siglades', 'delay_15']].copy()
    
    # Historical Operator Rate (Analogous to Rappi Partner Efficiency)
    historical_opera = df_temp.groupby('opera')['delay_15'].mean().reset_index()
    historical_opera.rename(columns={'delay_15': 'opera_historical_delay_rate'}, inplace=True)
    df = df.merge(historical_opera, on='opera', how='left')
    
    # Historical Destination Rate
    historical_dest = df_temp.groupby('siglades')['delay_15'].mean().reset_index()
    historical_dest.rename(columns={'delay_15': 'dest_historical_delay_rate'}, inplace=True)
    df = df.merge(historical_dest, on='siglades', how='left')
    
    return df

def impute_and_flag_missing(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Implements the Senior Robust Imputation: creates a missing indicator flag
    before imputing the column with the median.
    """
    # 1. Create the missing indicator flag
    df[f'{column}_is_missing'] = df[column].isnull().astype(int)
    
    # 2. Impute with the median
    df[column] = df[column].fillna(df[column].median())
    
    return df