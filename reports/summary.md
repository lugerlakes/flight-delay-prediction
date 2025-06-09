# Santiago Flight Delay Prediction – Full Challenge Solution

## Problem Overview

The goal was to **predict the probability of a flight delay over 15 minutes** for departures and arrivals at **Santiago Airport (SCL)** during 2017. The dataset includes flight schedules, operators, and metadata used to generate a binary classification target.

---

## 1. Data Exploration & Insights

Exploratory analysis included temporal and categorical variables:
- **Month, day of week, airline, flight type, and destination.**
- We used bar plots and heatmaps to identify delay patterns.

### Key Findings:
- Delay peaks occurred on **Mondays, Fridays, and holidays**.
- Some **airlines and destinations** consistently experienced more delays.
- **Strikes** showed a clear spike in delay probability (from ~18% to ~35%).

---

## 2. Feature Engineering

We engineered additional features and exported the processed dataset to `synthetic_features.csv`.

| Feature          | Description                                                     |
|------------------|-----------------------------------------------------------------|
| `high_season`    | Peak travel season in Chile                                     |
| `min_diff`       | Time difference between scheduled and actual departure          |
| `delay_15`       | Target: 1 if delay > 15 minutes, else 0                         |
| `period_day`     | Time slot (Morning, Afternoon, Night)                           |
| `is_holiday`     | 1 if flight is on a national holiday                            |
| `is_strike_day`  | 1 if flight date matches simulated strike schedule              |

---

## 3. Delay Behavior Analysis

We observed strong relationships between `delay_15` and the following:
- **Destination (`siglades`)**
- **Airline (`opera`)**
- **Flight type (`tipovuelo`)**
- **Calendar context (`is_holiday`, `is_strike_day`)**

These variables were selected as model features due to high correlation with the target.

---

## 4. Model Training & Threshold Tuning

Three supervised classifiers were trained using pipelines:

| Model                | Description                            |
|----------------------|----------------------------------------|
| `RandomForest`       | Tree-based ensemble                    |
| `LogisticRegression` | Linear, interpretable baseline         |
| `XGBoost`            | Gradient boosting for structured data  |

We also applied **threshold tuning** on Logistic Regression using the Precision-Recall curve, selecting an **optimal threshold of 0.48** to maximize F1 score and recall.

---

## 5. Evaluation Results

| Model                      | Accuracy | Recall | Precision | F1 Score | ROC AUC |
|---------------------------|----------|--------|-----------|----------|---------|
| LogisticRegression (0.48) | 60.0%    | **63.9%** | 26.0%    | **0.370** | 0.657   |
| RandomForest              | 70.0%    | 41.9%  | 28.7%    | 0.341    | 0.634   |
| XGBoost                   | **82.3%**| 11.0%  | **62.3%** | 0.186    | **0.705** |
| VotingClassifier (LR+RF)  | 71.3%    | 45.1%  | 31.0%    | 0.368    | 0.660   |

---

## 6. Model Interpretation

### ✅ Logistic Regression (Threshold = 0.48)
- Best F1 score and recall.
- Highly suitable if **recall is the priority** (i.e., identifying as many delays as possible).
- Benefits the most from added features like `is_holiday` and `is_strike_day`.

### 🌲 Random Forest
- Strong baseline with good accuracy and ROC AUC.
- Balanced but slightly lower recall than LR.
- Easy to interpret with feature importances.

### ⚙️ XGBoost
- Very high accuracy and AUC.
- **Extremely low recall** makes it impractical for this task.
- Suitable only if the priority is to **avoid false positives**.

### 🧠 VotingClassifier (RF + LR, threshold = 0.5)
- Combines strengths of both base models.
- Offers better recall than Random Forest, and better precision than LR alone.
- **Did not include the tuned threshold** in the ensemble (uses 0.5 by default).

---

## 7. Most Important Features

Feature analysis (e.g. from Random Forest):
- `is_strike_day`, `tipovuelo`, `period_day`, and `opera` were most influential.
- Added features provided meaningful context for the model to detect delays.

---

## 8. Recommendations & Next Steps

1. **Integrate External Data**  
   - Weather could further enhance accuracy.

2. **Deploy with Monitoring**  
   - Wrap best model in an API or dashboard (e.g., Streamlit).
   - Set up alerting for drift in delay patterns or drop in recall.