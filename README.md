# Operational Risk Prediction for Complex Logistics Networks

This predictive analytics project is designed to classify and predict the likelihood of an operational failure (e.g., flight delay > 15 minutes) in a complex logistics network. It uses real flight data from Santiago Airport (SCL) in 2017 as a case study for building a high-Recall alerting system.

The core focus is demonstrating a complete MLOps lifecycle, including robust feature engineering, cost-sensitive modeling, scalable API deployment (FastAPI/Modal), and continuous monitoring strategy (Airflow).

## Goals
- Operational Classification: Develop a classification model to predict high-risk operational status (delay_15) by optimizing for Recall (Sensitivity).
- Robust Feature Engineering: Create high-signal, causal features (e.g., historical operator efficiency) and implement robust data imputation using missingness indicator flags.
- Production Deployment: Serve predictions using a low-latency FastAPI backend containerized for serverless deployment (Modal).
- MLOps Strategy: Outline a comprehensive strategy for model maintenance, retraining, and Model Drift detection using an orchestrator like Apache Airflow.

## Project Structure
The project follows a modular, reproducible structure where logic is separated from experimentation.
```
flight-delay-prediction/
├── app/ # Deployment layer
│ ├── main.py # FastAPI backend for low-latency inference
│ └── streamlit_app.py # Streamlit UI for operational analysts
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
The prediction relies heavily on engineered features that capture historical efficiency and robustness:

| Feature Name        | Description                                                      | Rationale (Logistic Analogy) |
|---------------------|------------------------------------------------------------------| ---------------------------- |
|`opera_historical_delay_rate`| Average historical delay rate of the operating airline.| Partner Efficiency: Analogous to a restaurant or courier's historical latency. The strongest predictor of future risk.|
| `dest_historical_delay_rate`| Average historical delay rate of the destination route. | Route Congestion: Captures systemic issues related to a specific delivery zone or hub.|
| `tavg_is_missing`        | Binary flag (0/1) indicating if weather data was missing at the time of prediction. | Robustness: Ensures the model is resilient to production data quality issues (sensor/API failures)|
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
| Ingestion | Airflow | Orchestrates loading new daily/weekly order logs into the training data lake. |
| Validation | Airflow + Notebooks | Schedules a daily task to read prediction logs from FastAPI and execute the validation portion of 03_Model_Training_and_Evaluation.ipynb to detect performance drops (Model Drift). |
| Retraining Trigger | Airflow Logic | If the production Recall/ROC AUC metric falls below an operational threshold (e.g., 60%), Airflow automatically triggers the full retraining pipeline (Stage 1-3). |
| Artifact Update | Modal/Airflow | The new model artifacts (.pkl) are automatically persisted and pushed to the deployment environment, ensuring the live service uses the latest, most accurate model. |

---

## Model Metrics Summary
The project prioritized Recall (minimizing False Negatives, i.e., missed delays) over raw Accuracy, making it suitable for an operational alerting system.

| Metric | Rationale |
|-----|---------|
| Recall (Tuned LogReg) | ~65%+ @ 0.35 Threshold |
| Cost-Sensitive Learning | `class_weight='balanced'` |
| Robust Ensemble | Voting Classifier |

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
| FastAPI | `uvicorn app.main:app --reload` | Production-like inference API |
| Streamlit | `streamlit run app/streamlit_app.py` | Dispatcher/Analyst User Interface |
| Modal | `modal deploy modal_stub.py` | Serverless, scalable deployment |
---

### Impact & Results
This section summarizes the project's value from an operational decision-making perspective.

| Component | Description |
| --------- | ----------- |
| Situation | The system faced a high rate of undiagnosed operational failures (missed delays), leading to reactive damage control and poor service reliability. Failures were concentrated in high-risk operators and peak congestion periods. |
| Task | Build a predictive alerting tool capable of identifying high-risk events (delay > 15 min) before they occur, prioritizing the minimization of False Negatives (missed delays). |
| Action | - Data Rigor: Engineered causal features, such as the  `opera_historical_delay_rate `. 
- Model Calibration: Employed cost-sensitive learning and tuned the prediction threshold to 0.35 to optimize for Recall. 
- Deployment: Packaged the prediction logic into a low-latency FastAPI endpoint for real-time monitoring.|
| Result | The deployed system achieved a ~65% Recall rate at the operational threshold. This translates directly to an increased ability to proactively flag and mitigate two-thirds of critical operational failures, allowing teams to intervene (re-assign resources, notify stakeholders) and significantly improve the overall service reliability.|