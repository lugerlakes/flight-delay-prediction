import pandas as pd
import numpy as np

class RiskEncoder:
    """
    Handles target encoding for categorical features to prevent data leakage.
    Fits on training data, transforms test data.
    """
    def __init__(self, group_cols=['operating_airline', 'destination_city_name'], target_col='delay_15'):
        self.group_cols = group_cols
        self.target_col = target_col
        self.mappings = {}
        self.global_mean = 0

    def fit(self, df: pd.DataFrame):
        """Calculates historical rates from the TRAINING set only."""
        self.global_mean = df[self.target_col].mean()
        
        for col in self.group_cols:
            # Calculate mean delay per category
            stats = df.groupby(col)[self.target_col].mean()
            self.mappings[col] = stats
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies the calculated rates to a dataset (Train or Test)."""
        df = df.copy()
        for col in self.group_cols:
            new_col_name = f"{col}_historical_delay_rate"
            # Map the rates; fill unknowns (new airlines/destinations) with global mean
            df[new_col_name] = df[col].map(self.mappings[col]).fillna(self.global_mean)
        return df

def impute_and_flag_missing(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Creates a missing indicator flag before imputing the column with the median.
    """
    # 1. Create the missing indicator flag
    df[f'{column}_is_missing'] = df[column].isnull().astype(int)
    
    # 2. Impute with the median
    df[column] = df[column].fillna(df[column].median())
    
    return df