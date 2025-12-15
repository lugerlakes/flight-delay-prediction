# Operational Risk Prediction for Complex Logistics Networks (SCL Case Study)
This predictive analytics project is designed to classify and predict the likelihood of an operational failure (e.g., flight delay > 15 minutes) in a complex logistics network. It uses real flight data from Santiago Airport (SCL) in 2017 as a case study for building a high-Recall alerting system.

The core focus is demonstrating a complete MLOps lifecycle, including robust feature engineering, cost-sensitive modeling, scalable API deployment (FastAPI/Modal), and continuous monitoring strategy (Airflow).

## Goals
- Operational Classification: Develop a classification model to predict high-risk operational status (delay_15) by optimizing for Recall (Sensitivity).

- Robust Feature Engineering: Create high-signal, causal features (e.g., historical operator efficiency) and incorporate environmental variables (Wind/Pressure).

- Production Deployment: Serve predictions using a low-latency FastAPI backend containerized for serverless deployment (Modal).

- MLOps Strategy: Outline a comprehensive strategy for model maintenance, retraining, and Model Drift detection using an orchestrator like Apache Airflow.

## Project Structure
The project follows a modular, reproducible structure where logic is separated from experimentation.
```
flight-delay-prediction/
├── app/ # Deployment layer
│ ├── main.py # FastAPI backend for low-latency inference
│ └── streamlit_app.py # Streamlit UI for operational analysts
├── dags/ # Airflow Orchestration
│ ├── airflow_dag_retrain.py
├── data/ 
│ ├── raw/ # Original data
│ └── interim/ # Cleaned, Feature Engineered data (saved from Stage 1/2)
├── models/ # Serialized artifacts (.pkl)
│ ├── preprocessor_final.pkl # ColumnTransformer pipeline
│ └── voting_classifier_final.pkl # Final trained model
├── notebooks/ # Step-by-step documentation of the process (Stage 1-4)
│ ├── 01_Data_Acquisition_and_Cleaning.ipynb 
│ ├── 02_Exploratory_Data_Analysis_and_Feature_Engineering.ipynb
│ ├── 03_Model_Training_and_Evaluation.ipynb # Cost-sensitive modeling
│ └── 04_Model_Persistence_and_Deployment_Prep.ipynb # MLOps planning
├── reports/ # Figures and plots
 │ └── figures/ 
├── src/ # Modular source code (used by notebooks and FastAPI)
│ ├── data/
│ │ └── data_pipeline.py # Functions for loading and cleaning
│ └── features/
│ │ └── feature_engineering.py # Logic for historical rates and imputation
├── modal_stub.py # Serverless deployment definition for Modal
├── requirements.txt # Dependencies
└── README.md
```
---

## Key Features (Causal & Engineered)
The prediction relies on engineered features that capture historical efficiency and environmental context:

| Feature Name        | Description                                                      | Rationale (Logistic Analogy) |
|---------------------|------------------------------------------------------------------| ---------------------------- |
|`opera_historical_delay_rate`| Average historical delay rate of the operating airline.| Partner Efficiency: Analogous to a restaurant or courier's historical latency. The strongest predictor of future risk.|
| `dest_historical_delay_rate`| Average historical delay rate of the destination route. | Route Congestion: Captures systemic issues related to a specific delivery zone or hub.|
| `wspd / pres`        | Wind Speed (Knots) and Atmospheric Pressure. | Environmental Constraints: External factors that impact logistical flow. Validated via T-Test in Stage 3.|
| `period_day`     | Time bucket: morning, afternoon, night.|Capacity Strain: Captures accumulated delay and congestion peaks.|
| `delay_15`        | Target: 1 if delay > 15 minutes, else 0. |Cost-Sensitive Target: Focuses the model on critical failures (the minority class).|

---

## Deployment Strategy (MLOps)
The system is designed for scalable, decoupled deployment across two environments:

1. Real-Time Inference (FastAPI & Modal)
The prediction pipeline is exposed as a low-latency web service.

  - FastAPI Backend (app/main.py): Handles model loading, preprocessing (using preprocessor_final.pkl), and prediction. It uses a tuned operational threshold (0.35) to maximize alert sensitivity (Recall).
  - Streamlit UI (app/streamlit_app.py): Provides a simple analyst interface to input data and receive the operational alert (ALERT: High Delay Risk).
  - Serverless Deployment (modal_stub.py): Deploys both the FastAPI endpoint and the Streamlit frontend efficiently using Modal, ensuring scalability without managing infrastructure.

2. Model Maintenance (Apache Airflow Rationale)
Airflow is used to automate the full life cycle, ensuring the model's longevity and performance in a live environment.

| Stage | Tool/Goal | Rationale for Senior MLOps |
|-----|---------|--------------------------|
| Monitoring | Airflow Task | A custom Branch Operator checks the Production Recall weekly. If it drops below 0.60 (Drift), the retraining pipeline is triggered.|
| Ingestion | Airflow | Orchestrates loading new daily/weekly order logs into the training data lake. |
| Training | PythonOperator | Retrains the XGBoost classifier with updated data to capture new patterns (e.g., seasonal weather shifts).|
| Deployment | CI/CD | New artifacts (xgb_final.pkl) are automatically validated and pushed to the production volume. |

---

## Model Metrics Summary
We selected XGBoost as the Champion Model due to its superior ability to detect delays (Recall) compared to linear baselines and voting ensembles.

| Metric | Value | Rationale |
|-----|---------| -----------|
| Recall (Class 1) | ~78% | Primary KPI. Successfully identifies nearly 8 out of 10 delayed flights. |
| ROC-AUC | 0.71 | Robust discrimination capability despite high noise. |
| Threshold | 0.35 | Optimized cut-off point to balance Sensitivity vs. False Alarms |

---

## Installation
Requires **Python = 3.10**
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

### Run Prediction Apps
| App | Command | Purpose |
|-----|---------|-------- |
| FastAPI | `uvicorn app.main:app --reload` | Starts the inference engine at http://127.0.0.1:8000 |
| Streamlit Frontend | `streamlit run app/streamlit_app.py` | Launches the UI dashboard for testing |
| Modal Deploy | `modal deploy modal_stub.py` | Deploys backend to the cloud |
---

### Impact & Results
This section summarizes the project's value from an operational decision-making perspective.

| Component | Description |
| --------- | ----------- |
| Situation | The system faced a high rate of undiagnosed operational failures (missed delays), leading to reactive damage control and poor service reliability. |
| Task | Build a predictive alerting tool capable of identifying high-risk events (delay > 15 min) before they occur, prioritizing the minimization of False Negatives (missed delays). |
| Action | Implemented a Cost-Sensitive XGBoost model with engineered historical risk features. Validated the impact of weather variables (wind, pressure). Deployed via FastAPI with MLOps monitoring logic.|
| Result | The deployed system achieved a ~78% Recall rate at the operational threshold. This translates directly to an increased ability to proactively flag and mitigate the vast majority of critical delays, allowing teams to intervene (re-assign resources, notify stakeholders) effectively.|