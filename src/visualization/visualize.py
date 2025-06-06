import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
def plot_delay_rate_by_column(df, column, top_n=None, title=None, figsize=(10, 6)):
    """
    Plot average delay rate (delay_15) by category in a given column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing the column and 'delay_15' binary target.
    column : str
        Column to group by and analyze.
    top_n : int, optional
        If set, show only the top N categories by frequency.
    title : str, optional
        Plot title.
    figsize : tuple, optional
        Figure size.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Optional: restrict to top N categories
    if top_n:
        top_categories = df[column].value_counts().nlargest(top_n).index
        data = df[df[column].isin(top_categories)].copy()
    else:
        data = df.copy()

    # Compute delay rate per category
    rate = data.groupby(column)["delay_15"].mean().sort_values(ascending=False)

    # Plot
    plt.figure(figsize=figsize)
    sns.barplot(x=rate.values, y=rate.index, palette="Reds_r")
    plt.xlabel("Delay Rate (> 15 min)")
    plt.ylabel(column)
    plt.title(title or f"Delay Rate by {column}")
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.show()



def plot_count_by_column(df, column, title=None, figsize=(10, 6)):
    """
    Plot count of observations for a given categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset to plot.
    column : str
        Column to count values.
    title : str, optional
        Plot title.
    figsize : tuple, optional
        Size of the figure.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=figsize)
    order = df[column].value_counts().index
    sns.countplot(data=df, x=column, order=order, palette="Blues")

    plt.xlabel(column)
    plt.ylabel("Count")
    if title:
        plt.title(title)
    else:
        plt.title(f"Count by {column}")
    plt.xticks(rotation=45)
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
def plot_delay_rate_by_two_categories(df, cat1, cat2, title=None, top_n=None, figsize=(10, 6), palette="Reds"):
    """
    Plot delay rate (delay_15) as a heatmap grouped by two categorical features.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset with 'delay_15' column and the specified categorical columns.
    cat1 : str
        First categorical variable (rows in heatmap).
    cat2 : str
        Second categorical variable (columns in heatmap).
    title : str, optional
        Plot title.
    top_n : int, optional
        Show only the top N most frequent categories from cat1.
    figsize : tuple, optional
        Figure size.
    palette : str or colormap, optional
        Color palette for heatmap.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    data = df.copy()

    # Filter top N categories (based on frequency of cat1)
    if top_n:
        top_categories = data[cat1].value_counts().nlargest(top_n).index
        data = data[data[cat1].isin(top_categories)]

    # Create pivot table of delay rate
    heatmap_data = data.pivot_table(values="delay_15", index=cat1, columns=cat2, aggfunc="mean")

    plt.figure(figsize=figsize)
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=palette, linewidths=0.5)

    plt.title(title or f"Delay Rate: {cat1} vs {cat2}")
    plt.xlabel(cat2)
    plt.ylabel(cat1)
    plt.tight_layout()
    plt.show()

