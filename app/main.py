# FastAPI Deployment
# The objective is charge the artifacts (preprocessor and model) and expose an endpoint for inference in real time.

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

# --- 1. Load Artifacts ---
# Define the paths for the model artifacts
MODEL_PATH = '../models/voting_classifier_final.pkl'
PREPROCESSOR_PATH = '../models/preprocessor_final.pkl'
TARGET_THRESHOLD = 0.35 # Threshold tuned in Stage 3 for high Recall (Operational Alert)

try:
    # Load the fitted preprocessor pipeline
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    # Load the final trained model (Voting Classifier)
    model = joblib.load(MODEL_PATH)
    print("Model and Preprocessor loaded successfully.")
except FileNotFoundError as e:
    # This is critical for production robustness
    print(f"ERROR: Artifacts not found. Check model paths: {e}")
    # In a real app, this would prevent the server from starting.
    raise RuntimeError("Failed to load ML artifacts.")

# --- 2. Define Input Schema (Pydantic) ---
# This ensures data consistency and validation at the API entry point.
# Features MUST match those used in the training pipeline.

class FlightFeatures(BaseModel):
    # Core Flight/Logistics Features
    mes: int
    dianom: str  # Day of the week
    tipovuelo: str  # I or N
    opera: str  # Airline Operator
    siglades: str  # Destination Airport
    period_day: str  # Morning, Afternoon, Night
    
    # External / Engineered Features
    tavg: float  # Simulated Average Temperature
    # Note: tavg_is_missing, opera_historical_delay_rate, and dest_historical_delay_rate 
    # are calculated internally or added by the FE process before the preprocessor.
    # For a minimal API, we only accept features that a user/system would input.
    
    # If using historical rates directly, they must be passed:
    opera_historical_delay_rate: float
    dest_historical_delay_rate: float
    
    # For robust imputation:
    tavg_is_missing: int = 0 # Default to 0, or calculate dynamically if tavg is missing

# --- 3. FastAPI Initialization ---
app = FastAPI(
    title="Flight Delay Risk Prediction API (SCL)",
    description="Predictive Service for Operational Risk in Logistics (High Recall Focused)."
)

# --- 4. Prediction Endpoint ---
@app.post("/predict")
def predict_delay_risk(features: FlightFeatures):
    """
    Receives flight features and returns the probability and binary classification of delay (> 15 min).
    """
    try:
        # Convert Pydantic model to a DataFrame (required by the scikit-learn pipeline)
        input_data = features.model_dump()
        df_input = pd.DataFrame([input_data])
        
        # 1. Feature Engineering Step (Manually calculate/verify features if needed)
        # In a full production app, we would call a shared FE function here.
        # Since we are using the 'historical rate' features as direct inputs for simplicity,
        # we only need to ensure the order/types match the preprocessor.
        
        # 2. Preprocessing
        # This step handles scaling and One-Hot Encoding
        X_processed = preprocessor.transform(df_input)
        
        # 3. Prediction
        # Predict probability of delay (Class 1)
        proba_delay = model.predict_proba(X_processed)[:, 1][0]
        
        # 4. Classification based on Tuned Threshold (Operational Alert)
        is_delayed = int(proba_delay >= TARGET_THRESHOLD)
        
        # 5. Operational Recommendation
        action = "Monitor/Normal"
        if is_delayed == 1:
            action = "ALERT: High Delay Risk (Flag for Mitigation)"
            
        # Log prediction for MLOps monitoring (In a real system, this goes to a database)
        # print(f"LOG: Proba={proba_delay:.4f}, Alert={is_delayed}, Action={action}")

        return {
            "prediction_status": "Success",
            "probability_of_delay": round(proba_delay, 4),
            "predicted_class": is_delayed,
            "threshold_used": TARGET_THRESHOLD,
            "operational_action": action
        }
        
    except Exception as e:
        # Catch any pipeline or prediction errors for debugging
        raise HTTPException(status_code=500, detail=f"Prediction failed due to: {e}")

# To run the app: uvicorn app.main:app --reload