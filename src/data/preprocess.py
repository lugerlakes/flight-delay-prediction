import pandas as pd

def sanitize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names to snake_case (lowercase and underscores).
    This ensures consistency even if the input CSV has 'Scheduled_Departure' or 'scheduled departure'.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace("-", "_").str.replace(" ", "_")
    return df

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts specific time columns to datetime objects.
    Expects standardized English column names.
    """
    df = df.copy()

    date_cols = ['scheduled_departure', 'actual_departure']
    
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def report_nulls(df: pd.DataFrame):
    """Prints a summary of missing values."""
    null_summary = df.isnull().sum()
    if null_summary.sum() > 0:
        print("Missing values by column:")
        print(null_summary[null_summary > 0])
    else:
        print("No missing values found.")