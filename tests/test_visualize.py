import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pandas as pd
from src.data.load_data import load_raw_data
from src.data.preprocess import parse_dates, clean_column_names
from src.features.build_features import build_synthetic_features
from src.visualization.visualize import (
    plot_delay_rate_by_column,
    plot_count_by_column,
    plot_delay_distribution
)

def main():
    # Load and prepare the data
    df = load_raw_data()
    df = parse_dates(df)
    df = clean_column_names(df)
    df = build_synthetic_features(df)

    print("✅ Data loaded and features generated. Now plotting...")

    # Plot examples
    plot_delay_rate_by_column(df, "opera")        # Delay rate by airline
    plot_delay_rate_by_column(df, "siglades")     # Delay rate by destination
    plot_count_by_column(df, "period_day")        # Flight distribution by period
    plot_delay_distribution(df)                   # Distribution of delay in minutes

if __name__ == "__main__":
    main()
