import pandas as pd

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Fecha-I"] = pd.to_datetime(df["Fecha-I"], errors="coerce")
    df["Fecha-O"] = pd.to_datetime(df["Fecha-O"], errors="coerce")
    return df

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace("-", "_")
    return df

def report_nulls(df: pd.DataFrame):
    null_summary = df.isnull().sum()
    print("Missing values by column:")
    print(null_summary[null_summary > 0])
