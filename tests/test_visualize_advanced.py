import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.data.load_data import load_raw_data
from src.data.preprocess import parse_dates, clean_column_names
from src.features.build_features import build_synthetic_features
from src.visualization.visualize import plot_delay_rate_by_two_categories

def main():
    # Load and prepare the dataset
    df = load_raw_data()
    df = parse_dates(df)
    df = clean_column_names(df)
    df = build_synthetic_features(df)

    print("✅ Dataset ready for advanced visualizations.")

    # Plot 1: Delay rate by airline and type of flight
    print("📊 Delay rate by airline and flight type...")
    plot_delay_rate_by_two_categories(
        df,
        category_x="opera",
        category_hue="tipovuelo",
        top_n=10,
        save_path="reports/figures/delay_by_opera_and_tipovuelo.png"
    )

    # Plot 2: Delay rate by destination and high season
    print("📊 Delay rate by destination and season...")
    plot_delay_rate_by_two_categories(
        df,
        category_x="siglades",
        category_hue="high_season",
        top_n=10,
        save_path="reports/figures/delay_by_siglades_and_highseason.png"
    )

if __name__ == "__main__":
    main()
