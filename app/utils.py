# app/utils.py — Shared Preprocessing + Logging Logic

import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
LOG_PATH = os.getenv("LOG_PATH", "logs/predictions_log.csv")

def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = ["dianom", "tipovuelo", "opera", "siglades", "period_day"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df

def log_prediction(input_data, prediction, probability, model_name):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    log_row = pd.DataFrame([{
        **input_data,
        "predicted_delay": prediction,
        "delay_probability": probability,
        "model": model_name,
        "timestamp": datetime.now().isoformat()
    }])

    if not os.path.exists(LOG_PATH):
        log_row.to_csv(LOG_PATH, index=False)
    else:
        log_row.to_csv(LOG_PATH, mode="a", header=False, index=False)
