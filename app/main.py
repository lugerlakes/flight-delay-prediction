# FastAPI Deployment
# The objective is charge the artifacts (preprocessor and model) and expose an endpoint for inference in real time.

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# --- 1. Load Artifacts ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')

# CAMBIO CRÍTICO: Usamos el modelo XGBoost directamente porque tuvo mejor Recall (0.78)
# que el Ensamble (0.59). Es más ligero y efectivo.
MODEL_PATH = os.path.join(MODELS_DIR, 'xgb_final.pkl')
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, 'preprocessor_final.pkl')

# Operational Threshold (Optimizado en Stage 3 para XGBoost)
TARGET_THRESHOLD = 0.35 

try:
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    print(f"✅ XGBoost Model and Preprocessor loaded from {MODELS_DIR}")
except FileNotFoundError as e:
    print(f"❌ CRITICAL ERROR: Artifacts not found. Details: {e}")
    model = None
    preprocessor = None

# --- 2. Define Input Schema ---
class FlightFeatures(BaseModel):
    # Categorical Features
    operating_airline: str
    destination_city_name: str
    period_day: str
    day_of_week_name: str
    flight_type: str
    
    # Numerical / Time Features
    month: int
    
    # Weather Features
    wspd: float
    pres: float
    
    # Risk Features
    opera_historical_delay_rate: float
    dest_historical_delay_rate: float

    # Optional flags
    wspd_is_missing: int = 0
    pres_is_missing: int = 0

# --- 3. FastAPI App ---
app = FastAPI(
    title="SCL Flight Delay Predictor (XGBoost)",
    description="API exposing the Champion XGBoost model. Optimized for High Recall.",
    version="1.0.0"
)

@app.post("/predict")
def predict_delay_risk(features: FlightFeatures):
    if not model or not preprocessor:
        raise HTTPException(status_code=503, detail="Model artifacts are not loaded.")

    try:
        # 1. Prepare Data
        input_dict = features.dict()
        
        # Robustness: Handle Missing Weather Placeholders
        if input_dict['wspd'] == -999:
            input_dict['wspd_is_missing'] = 1
            input_dict['wspd'] = 0 
        
        if input_dict['pres'] == -999:
            input_dict['pres_is_missing'] = 1
            input_dict['pres'] = 0

        df_input = pd.DataFrame([input_dict])
        
        # 2. Preprocessing
        X_processed = preprocessor.transform(df_input)
        
        # 3. Inference (XGBoost)
        # XGBoost output is probability of class 1
        proba_delay = model.predict_proba(X_processed)[:, 1][0]
        
        # 4. Business Logic
        is_delayed = int(proba_delay >= TARGET_THRESHOLD)
        
        return {
            "prediction": "DELAY" if is_delayed == 1 else "ON-TIME",
            "confidence_score": round(proba_delay, 4),
            "threshold_used": TARGET_THRESHOLD,
            "risk_level": "HIGH" if is_delayed == 1 else "LOW",
            "model_used": "XGBoost Classifier"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")
# To run the app: uvicorn app.main:app --reload