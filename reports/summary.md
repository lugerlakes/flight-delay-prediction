
# Santiago Flight Delay Prediction – Full Challenge Solution

## Problem Overview

The objective was to **predict the probability of delay** for flights **taking off or landing at Santiago's Airport (SCL)** during 2017. The dataset includes scheduled and operational metadata per flight, and the ultimate target is whether a delay of more than 15 minutes occurred.

---

## 1. Data Distribution & Exploratory Analysis

We performed exploratory data analysis (EDA) on categorical and temporal variables such as:
- **Destination city**, **airline**, **day of week**, **month**, **type of flight** (national/international).
- We visualized flight distributions and delay rates across those dimensions using bar plots and heatmaps.

### Key Insights:
- Certain **airlines and destinations** had significantly higher delay rates.
- **Mondays and Fridays** showed elevated delays, likely due to business traffic.
- **September and December** displayed increased variation due to holiday peaks.

---

## 2. Feature Engineering (Synthetic Columns)

We created the following **synthetic features** and exported the resulting dataset to `synthetic_features.csv`:

| Feature         | Description                                                                 |
|----------------|-------------------------------------------------------------------------------|
| `high_season`  | 1 if flight falls in Chilean peak travel periods, else 0                     |
| `min_diff`     | Difference (in minutes) between scheduled and actual flight time             |
| `delay_15`     | 1 if `min_diff > 15`, otherwise 0 (binary classification target)             |
| `period_day`   | Morning (5–11:59), Afternoon (12–18:59), Night (19–4:59) from scheduled time |
| `is_holiday`   | 1 if flight is on a Chilean national holiday                                 |
| `is_strike_day`| 1 if flight occurred during simulated known strike dates                     |

---

## 3. Delay Behavior Across Variables

We analyzed `delay_15` against categorical features:

- **Destination (`siglades`)**: Some cities showed chronically higher delay rates.
- **Airline (`opera`)**: Budget carriers had higher average delays.
- **Month & day of week**: Clear peaks around weekends and public holidays.
- **Flight type (`tipovuelo`)**: National flights experienced more delays than international ones.
- **Strikes** had a strong correlation with delay spikes (from ~18% to ~35%).

These variables were selected for modeling due to their strong association with the target.

---

## 4. Model Training

We trained three classifiers using pipelines with preprocessing:

| Model              | Description                            |
|-------------------|----------------------------------------|
| `RandomForest`     | Tree-based ensemble classifier          |
| `LogisticRegression`| Linear, interpretable baseline         |
| `XGBoost`          | Gradient-boosted trees with fine control|

Each model was trained on the enriched dataset and evaluated with the same test split.

---

## 5. Model Evaluation

### Metrics Used:
- **Accuracy**: General correctness
- **Recall**: Sensitivity to true delays (priority)
- **Precision**: Avoidance of false positives
- **F1 Score**: Harmonic mean of precision & recall
- **ROC AUC**: Overall class separability

### Results Summary:

| Model              | Accuracy | Recall | Precision | F1 Score | ROC AUC |
|-------------------|----------|--------|-----------|----------|---------|
| LogisticRegression| 63.0%    | **58.3%** | 26.9%    | **0.368** | 0.657   |
| RandomForest      | 70.0%    | 41.9%  | 28.7%    | 0.341    | 0.634   |
| XGBoost           | **82.3%**| 11.0%  | **62.3%** | 0.186    | **0.705** |

### Best Model:
- **Logistic Regression** had the **highest F1 Score**, making it the most balanced and reliable model for predicting delays in practice.
- XGBoost, while high in AUC, failed to detect delays (low recall), and would underperform operationally.

---

## Most Influential Variables

According to feature importance and correlation analysis:
- `is_strike_day` was highly predictive.
- `tipovuelo`, `period_day`, `opera`, and `siglades` were key categorical drivers.
- The addition of calendar-based variables improved **recall and F1 score**, proving the value of context.

---

## Suggested Improvements & Next Steps

1. **Threshold Tuning** – Adjust probability cutoff to better balance precision/recall.
    - We'll explore how changing the default decision threshold (usually 0.5) affects precision and recall. This involves:
    - Plotting the Precision-Recall vs Threshold curve
    - Finding an optimal point based on your business goal (e.g., minimizing false negatives)
    - Updating predictions using this tuned threshold
2. **Model Ensembling** – Try a VotingClassifier to mix logistic + random forest.
    - Train both base models
    - Wrap them in a VotingClassifier with voting='soft'
    - Evaluate with the same metrics (F1, AUC, etc.)
3. **External Data** – Integrate real weather data of SCEL (METAR/TAF historical data or public climate archives).
4. **Deployment** – Serve the model via API or Streamlit dashboard. Track performance over time. 
---
