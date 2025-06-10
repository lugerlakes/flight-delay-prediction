# Shared Preprocessing + Logging Logic

import pandas as pd
import os
from datetime import datetime

def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = ["dianom", "tipovuelo", "opera", "siglades", "period_day"]
    df[cat_cols] = df[cat_cols].astype("category")
    return df

def log_prediction(input_data, prediction, probability, model_name):
    log_path = "../logs/predictions_log.csv"
    df_log = pd.DataFrame([{
        **input_data,
        "predicted_delay": prediction,
        "delay_probability": probability,
        "model": model_name,
        "timestamp": datetime.now().isoformat()
    }])

    if not os.path.exists(log_path):
        df_log.to_csv(log_path, index=False)
    else:
        df_log.to_csv(log_path, mode="a", header=False, index=False)
