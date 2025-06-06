import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
def plot_delay_rate_by_column(df: pd.DataFrame, column: str, target: str = "delay_15", figsize=(12, 6)):
    plt.figure(figsize=figsize)
    order = df.groupby(column)[target].mean().sort_values(ascending=False).index
    ax = sns.barplot(
        data=df,
        x=column,
        y=target,
        order=order,
        palette="Blues_d",
        edgecolor=".2"
    )
    title_col = column.replace('_', ' ').title()
    ax.set_title(f"Average Delay Rate by {title_col}", fontsize=14, fontweight="bold")
    ax.set_xlabel(title_col, fontsize=12)
    ax.set_ylabel("Proportion of Delays > 15min", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    plt.tight_layout()
    plt.show()



def plot_count_by_column(df: pd.DataFrame, column: str, figsize=(10, 5)):
    plt.figure(figsize=figsize)
    ax = sns.countplot(
        data=df,
        x=column,
        order=df[column].value_counts().index,
        palette="pastel"
    )
    ax.set_title(f"Flight count by {column}", fontsize=14, fontweight="bold")
    ax.set_xlabel(column.capitalize(), fontsize=12)
    ax.set_ylabel("Flight Count", fontsize=12)
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    plt.show()

def plot_delay_distribution(df: pd.DataFrame, figsize=(12, 5)):
    plt.figure(figsize=figsize)
    ax = sns.histplot(df["min_diff"], bins=100, kde=True, color="#4c72b0", alpha=0.8)
    plt.axvline(15, color="red", linestyle="--", linewidth=2, label="15 min threshold")
    ax.set_title("Distribution of Flight Delays (min_diff)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Delay in Minutes", fontsize=12)
    ax.set_ylabel("Number of Flights", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_delay_rate_by_two_categories(
    df: pd.DataFrame,
    category_x: str,
    category_hue: str,
    target: str = "delay_15",
    top_n: int = 10,
    figsize=(12, 6),
    save_path: str = None
):
    top_categories = df[category_x].value_counts().head(top_n).index
    df_plot = df[df[category_x].isin(top_categories)]

    plt.figure(figsize=figsize)
    ax = sns.barplot(
        data=df_plot,
        x=category_x,
        y=target,
        hue=category_hue,
        estimator="mean",
        palette="Set2"
    )
    ax.set_title(f"Average Delay Rate by {category_x.title()} and {category_hue.title()}", fontsize=14, fontweight="bold")
    ax.set_xlabel(category_x.replace("_", " ").title(), fontsize=12)
    ax.set_ylabel("Proportion of Delays > 15min", fontsize=12)
    ax.tick_params(axis="x", rotation=45)
    plt.legend(title=category_hue.replace("_", " ").title())

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"✅ Plot saved to: {save_path}")

    plt.show()
