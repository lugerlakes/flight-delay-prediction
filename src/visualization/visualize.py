import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay

sns.set(style="whitegrid")

def plot_delay_rate_by_column(df, column, top_n=None, title=None, figsize=(10, 6)):
    """
    Plot average delay rate (delay_15) by category in a given column.
    """
    if top_n:
        top_categories = df[column].value_counts().nlargest(top_n).index
        data = df[df[column].isin(top_categories)].copy()
    else:
        data = df.copy()

    rate = data.groupby(column)["delay_15"].mean().sort_values(ascending=False)

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
    """
    plt.figure(figsize=figsize)
    order = df[column].value_counts().index
    sns.countplot(data=df, x=column, order=order, palette="Blues")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.title(title or f"Count by {column}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_delay_distribution(df: pd.DataFrame, figsize=(12, 5)):
    """
    Plot histogram of min_diff values with 15-min delay threshold.
    """
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
    """
    data = df.copy()
    if top_n:
        top_categories = data[cat1].value_counts().nlargest(top_n).index
        data = data[data[cat1].isin(top_categories)]

    heatmap_data = data.pivot_table(values="delay_15", index=cat1, columns=cat2, aggfunc="mean")

    plt.figure(figsize=figsize)
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=palette, linewidths=0.5)
    plt.title(title or f"Delay Rate: {cat1} vs {cat2}")
    plt.xlabel(cat2)
    plt.ylabel(cat1)
    plt.tight_layout()
    plt.show()



def plot_model_metrics_comparison(results_dict):
    """
    Plot grouped bar chart comparing Accuracy, Recall, Precision and F1 Score across models.

    Parameters
    ----------
    results_dict : dict
        Dictionary with model names as keys and metrics as sub-dictionaries.
    """
    # Convert dict to DataFrame
    metrics_df = pd.DataFrame(results_dict).T.reset_index().rename(columns={"index": "model"})

    # Melt for seaborn plotting
    melt_df = metrics_df.melt(id_vars="model", 
                              value_vars=["accuracy", "recall", "precision", "f1_score"], 
                              var_name="metric", value_name="value")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=melt_df, x="metric", y="value", hue="model")
    plt.title("Comparison of Evaluation Metrics by Model")
    plt.ylabel("Score")
    plt.xlabel("Metric")
    plt.ylim(0, 1.0)
    plt.legend(title="Model")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()



def plot_feature_importances(model, feature_names, top_n=20, title="Feature Importances"):
    """
    Plot top N feature importances for a trained model.
    """
    importances = model.named_steps["classifier"].feature_importances_
    feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:top_n]
    labels, values = zip(*feat_imp)

    plt.figure(figsize=(10, 6))
    plt.barh(labels[::-1], values[::-1], color="orange")
    plt.xlabel("Importance")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(model, X_test, y_test, title="Confusion Matrix"):
    """
    Plot confusion matrix for a trained classification model.
    """
    plt.figure(figsize=(6, 6))
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap="Blues", values_format="d")
    plt.title(title)
    plt.tight_layout()
    plt.show()
