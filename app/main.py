# FastAPI Inference API

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from datetime import datetime
from app.utils import preprocess_input, log_prediction

app = FastAPI()

# Load models
models = {
    "logistic_regression": joblib.load("../models/logistic_regression.pkl"),
    "random_forest": joblib.load("../models/random_forest.pkl"),
    "xgboost": joblib.load("../models/xgboost.pkl"),
    "voting_classifier": joblib.load("../models/voting_classifier.pkl")
}

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
def predict_delay(flight: FlightInput, model_name: str = "logistic_regression"):
    if model_name not in models:
        return {"error": "Invalid model name. Choose from: logistic_regression, random_forest, xgboost, voting_classifier"}

    model = models[model_name]
    input_df = pd.DataFrame([flight.dict()])
    X_input = preprocess_input(input_df)

    prob = model.predict_proba(X_input)[0][1]
    pred = int(prob >= 0.48 if model_name == "logistic_regression" else 0.5)

    log_prediction(flight.dict(), pred, prob, model_name)

    return {
        "delay_probability": prob,
        "predicted_class": pred,
        "model_used": model_name
    }
