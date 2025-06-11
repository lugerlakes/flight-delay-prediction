# app/main.py — FastAPI Inference API

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from app.utils import preprocess_input, log_prediction

# Load environment variables
load_dotenv()

MODEL_DIR = os.getenv("MODEL_DIR", "models")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "logistic_regression")

app = FastAPI(title="✈️ SCL Flight Delay Predictor API")

# Load models
model_paths = {
    "logistic_regression": os.path.join(MODEL_DIR, "logistic_regression.pkl"),
    "random_forest": os.path.join(MODEL_DIR, "random_forest.pkl"),
    "xgboost": os.path.join(MODEL_DIR, "xgboost.pkl"),
    "voting_classifier": os.path.join(MODEL_DIR, "voting_classifier.pkl")
}

models = {}
for name, path in model_paths.items():
    if os.path.exists(path):
        models[name] = joblib.load(path)
    else:
        raise FileNotFoundError(f"❌ Model file missing: {path}")

class FlightInput(BaseModel):
    mes: int
    dianom: str
    tipovuelo: str
    opera: str
    siglades: str
    period_day: str
    high_season: int
    is_holiday: int
    is_strike_day: int
    tavg: float
    tmin: float
    tmax: float

class PredictionOutput(BaseModel):
    delay_probability: float
    predicted_class: int
    model_used: str

@app.post("/predict", response_model=PredictionOutput)
def predict_delay(flight: FlightInput, model_name: str = Query(DEFAULT_MODEL)):
    if model_name not in models:
        raise HTTPException(status_code=400, detail=f"Invalid model name: {model_name}")

    model = models[model_name]
    input_df = pd.DataFrame([flight.dict()])

    try:
        X_input = preprocess_input(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")

    try:
        prob = model.predict_proba(X_input)[0][1]
        threshold = 0.48 if model_name == "logistic_regression" else 0.5
        pred = int(prob >= threshold)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    log_prediction(flight.dict(), pred, prob, model_name)

    return {
        "delay_probability": prob,
        "predicted_class": pred,
        "model_used": model_name
    }
