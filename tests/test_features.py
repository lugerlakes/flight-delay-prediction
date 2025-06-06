import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.data.load_data import load_raw_data
from src.data.preprocess import parse_dates, clean_column_names
from src.features.build_features import build_synthetic_features, export_features

def main():
    # Load and preprocess
    df = load_raw_data()
    df = parse_dates(df)
    df = clean_column_names(df)

    # Generate synthetic features
    df = build_synthetic_features(df)

    # Preview result
    print("✅ Synthetic features added:")
    print(df[["fecha_i", "fecha_o", "min_diff", "delay_15", "high_season", "period_day"]].head())

    # Export
    export_features(df)

if __name__ == "__main__":
    main()