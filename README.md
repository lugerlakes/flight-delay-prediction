# Flight Delay Prediction

Predictive analytics project aimed at estimating the likelihood of delays in flights operated from/to Santiago Airport (SCL) in 2017. Includes exploratory data analysis, feature engineering, supervised model training, and robust evaluation with a reproducible approach.

## Goals
- Analyze flight delays at SCL airport during 2017
- Create meaningful synthetic features
- Train classification models to predict delays
- Evaluate performance and identify key drivers of delay

## Project Structure
```
flight-delay-prediction/
├── data/ # Original and processed datasets
│ ├── raw/ # Raw CSV files (original flight data)
│ └── processed/ # Cleaned data with engineered features
├── models/ # Serialized trained models
├── notebooks/ # Jupyter notebooks for EDA and modeling
│ └── solution.ipynb # Main notebook with full workflow
├── reports/ # Final reports and visualizations
│ └── figures/ # Saved plots from EDA and modeling
├── src/ # Modular source code for reuse
│ ├── init.py
│ ├── data/ # Data loading and preprocessing logic
│ │ ├── load_data.py
│ │ └── preprocess.py
│ ├── features/ # Feature engineering scripts
│ │ └── build_features.py
│ ├── models/ # Training and evaluation scripts
│ │ ├── train_model.py
│ │ └── evaluate_model.py
│ └── visualization/ # Custom visualizations
│ └── visualize.py
├── tests/ # Unit and integration tests
│ ├── test_features.py
│ ├── test_visualize.py
│ └── test_visualize_advanced.py
├── .gitignore # Files/folders to exclude from git
├── LICENSE # Project license
├── README.md # Project overview and documentation
└── requirements.txt # Project dependencies
```
---
## Installation
This project requires **Python = 3.10**
1. Clone the repository:
```bash
   git clone https://github.com/lugerlakes/flight-delay-prediction.git
   cd flight-delay-prediction
```
2. Create and activate a virtual environment
- (Option A) with venv:
```bash
    python -m venv .flight-delay-prediction
    .\.flight-delay-prediction\Scripts\activate  # On Windows
    source .flight-delay-prediction/bin/activate # On macOS/Linux
```
- (Option B) Or use conda:
```bash
    conda create --name flight-delay-prediction python=3.10
    conda activate flight-delay-prediction
```
3. Install dependencies:
```bash
    pip install -r requirements.txt
```
---

### Key Dependencies
- Python:
    - pandas
    - numpy
    - matplotlib
    - seaborn
    - scikit-learn
    - xgboost
    - jupyter

## How to Run

### Exploratory Analysis and Modeling

Open the notebook:
```bash
jupyter notebook notebooks/solution.ipynb
```
Follow the sections for:

- Data loading and cleaning

- Feature engineering

- Exploratory data analysis (EDA)

- Model training and evaluation

## Run tests and visualizations
From the project root:
```bash
# Run feature pipeline test
python tests/test_features.py
```
```bash
# Run EDA visualizations
python tests/test_visualize.py
```
```bash
# Run advanced grouped plots
python tests/test_visualize_advanced.py
```
Visual outputs will be saved to reports/figures/.


# ✈️ Flight Delay Prediction – SCL 2017

This project predicts the likelihood of a flight being delayed more than 15 minutes at **Arturo Merino Benítez Airport (SCL), Santiago, Chile**, using real 2017 data.

It is designed with **operational deployment in mind**, aiming to support **airline operations teams** in **real-time delay risk prediction** based on scheduled flight metadata, enriched with contextual variables (holidays, strikes, weather) and multiple predictive models.

---

## Goals

- Understand operational patterns of commercial flight delays at SCL.
- Create enriched synthetic features for temporal and contextual variability.
- Train, evaluate, and compare multiple supervised learning models.
- Expose a prediction interface via **FastAPI** and **Streamlit** for real-world airline use.
- Enable delay prediction based on flight details: airline, route, time, seasonality, and weather.
- Log predictions for future **monitoring** and **retraining**.

---

## Project Structure
```
flight-delay-prediction/
├── app/ # Deployment layer: FastAPI + Streamlit apps
│ ├── main.py # FastAPI backend for prediction
│ ├── streamlit_app.py # Streamlit UI
│ └── utils.py # Shared preprocessing & logging utils
├── data/ # Flight and weather data
│ ├── raw/ # Raw flight and weather files
│ └── processed/ # Cleaned & feature-engineered datasets
├── models/ # Serialized trained models (.pkl)
├── logs/ # Logs of predictions for monitoring
│ └── predictions_log.csv
├── notebooks/ # Jupyter notebook for full workflow
│ └── flight_delay_prediction.ipynb
├── reports/ # Figures and metrics
│ ├── figures/ # Visualizations (EDA, metrics)
│ └── summary.md # Final write-up
├── src/ # Modular source code (EDA, features, models, visualization)
│ ├── data/
│ ├── features/
│ ├── models/
│ └── visualization/
├── tests/ # Unit tests
│ ├── test_features.py
│ ├── test_visualize.py
│ └── test_visualize_advanced.py
├── modal_stub.py # Optional Modal deployment entrypoint
├── requirements.txt # Dependencies
├── .gitignore
├── LICENSE
└── README.md
```
---

## Deployment Strategy

This project includes two deployable applications:

### 🔹 FastAPI Backend (`app/main.py`)

- `POST /predict`: accepts a JSON payload of flight features
- Returns: predicted probability of delay and class (0 = on time, 1 = delayed)
- Supports model selection (logistic_regression, voting_classifier, etc.)
- Logs predictions to `logs/predictions_log.csv`

### 🔹 Streamlit UI (`app/streamlit_app.py`)

- User-friendly form to input flight data
- Calls FastAPI backend
- Displays:
  - Delay probability
  - Binary class
  - Recommended action (e.g., flag/monitor)
- Model selection available from dropdown

---

## Features

| Feature Name        | Description                                                      |
|---------------------|------------------------------------------------------------------|
| `delay_15`          | Target: 1 if delay > 15 mins, else 0                             |
| `high_season`       | Chilean seasonal peak flag (Dec–Mar, July, September holidays)   |
| `is_holiday`        | 1 if the date is a national holiday                              |
| `is_strike_day`     | 1 if a strike affected operations that day                       |
| `period_day`        | Time bucket: morning, afternoon, night                           |
| `weather` (avg, min, max) | Historical weather conditions for SCL                    |

---

## Installation

**Requires Python 3.10**

```bash
git clone https://github.com/lugerlakes/flight-delay-prediction.git
cd flight-delay-prediction
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```


### Run the Notebook (Modeling & Analysis)
```bash
jupyter notebook notebooks/flight_delay_prediction.ipynb
```
Includes:
- Exploratory analysis
- Feature engineering
- Model training: Logistic Regression, Random Forest, XGBoost, Voting Classifier
- Threshold tuning (recall-focused)
- Evaluation metrics and plots

### Run Prediction Apps
#### Option 1: FastAPI (localhost API)
```bash
uvicorn app.main:app --reload
```
Then visit: http://127.0.0.1:8000/docs

#### Option 2: Streamlit UI (form interface)
```bash
streamlit run app/streamlit_app.py
```
### Sample JSON Input
```json
{
  "mes": 9,
  "dianom": "Viernes",
  "tipovuelo": "N",
  "opera": "Sky Airline",
  "siglades": "Antofagasta",
  "period_day": "afternoon",
  "high_season": 1,
  "is_holiday": 1,
  "is_strike_day": 0,
  "tavg": 15.4,
  "tmin": 12.3,
  "tmax": 21.7
}
```
## Metrics Summary (Model Selection)

| Model                           | Accuracy | Recall | Precision | F1 Score | ROC AUC | Key Insight                                                 |
|--------------------------------|----------|--------|-----------|----------|---------|-------------------------------------------------------------|
| Logistic Regression (tuned)    | 59.7%    | **63.9%** | 26.0%    | **0.369** | 0.657   | Highest sensitivity to delayed flights                      |
| Voting Classifier              | **71.3%**| 45.1%  | 31.0%    | **0.368** | **0.660** | Balanced and robust ensemble performance                    |
| Logistic Regression (default)  | 63.0%    | 58.3%  | 26.9%    | **0.368** | 0.657   | Transparent and effective without threshold tuning          |
| Random Forest                  | 70.0%    | 41.9%  | 28.7%    | 0.341    | 0.634   | Interpretable and stable under different scenarios          |
| XGBoost                        | 82.3%    | 11.0%  | **62.3%** | 0.186    | **0.705** | High AUC, but impractical for delay detection due to low recall |

## Future Work
- Monitor model drift using prediction logs
- Schedule periodic retraining with updated data

## Operational Use Case
Airline schedulers or dispatchers can use this tool to:
- Estimate risk of delay before flight execution
- Flag high-risk flights for rescheduling, buffering, or monitoring
- Improve on-time performance (OTP) by incorporating historical risk patterns
- Proactively act on holiday or strike day effects