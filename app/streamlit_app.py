import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib

# --- 1. Configuration and Artifact Loading ---

# Streamlit App Title and Description
st.set_page_config(page_title="Flight Delay Risk Classifier", layout="wide")

# Load artifacts for reference/static features (NOTE: In production, Streamlit would call FastAPI)
try:
    PREPROCESSOR_PATH = '../models/preprocessor_final.pkl'
    # We load the preprocessor just to get the list of unique categories (airlines, destinations)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    # Extract categories from the 'cat' transformer (assuming index 1)
    ohe_transformer = preprocessor.named_transformers_['cat']
    
    # We must extract the original values for dropdowns (Simulating dynamic list from DB)
    # NOTE: The OHE categories include the feature name prefix (e.g., 'cat__opera_LATAM')
    
    # Placeholder lists based on typical SCL data (replace with actual loaded categories if possible)
    AIRLINES = ['Latin American Wings', 'JetSmart SPA', 'American Airlines', 'LATAM AIRLINES GROUP']
    DESTINATIONS = ['Buenos Aires', 'Miami', 'Antofagasta', 'Lima']
    PERIODS = ['morning', 'afternoon', 'night']
    DIAS = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

except FileNotFoundError:
    st.error("Error: Model artifacts not found. Using placeholder data.")
    AIRLINES = ['Airline A', 'Airline B']
    DESTINATIONS = ['Dest X', 'Dest Y']
    PERIODS = ['morning', 'afternoon', 'night']
    DIAS = ['Monday', 'Tuesday', 'Wednesday']


st.title("✈️ Operational Risk Classifier (SCL Flight Delay)")
st.subheader("Simulación: Predicción de Riesgo de Retraso de Pedido/Vuelo")
st.markdown("---")

# --- 2. Input Form (Dispatcher Interface) ---

with st.form("risk_prediction_form"):
    st.markdown("**Datos Operacionales del Vuelo/Pedido**")
    
    col1, col2 = st.columns(2)
    with col1:
        # Analogous to selecting the Restaurant/Courier
        selected_opera = st.selectbox("Airline Operator (OPERA):", AIRLINES)
        # Analogous to delivery zone
        selected_dest = st.selectbox("Destination (SIGLADES):", DESTINATIONS)
        # Analogous to time bucket (Crucial Feature)
        selected_period = st.selectbox("Time Period (PERIOD_DAY):", PERIODS)
    
    with col2:
        selected_dianom = st.selectbox("Day of the Week (DIANOM):", DIAS)
        selected_tipovuelo = st.selectbox("Flight Type (TIPOVUELO):", ['I', 'N']) # International/National
        # Month (Simulated input)
        selected_mes = st.slider("Month (MES):", 1, 12, 6)
    
    st.markdown("---")
    st.markdown("**Datos Externos y Históricos (Valores de ejemplo)**")
    
    col3, col4 = st.columns(2)
    with col3:
        # TAVG (Simulated Weather Data)
        selected_tavg = st.slider("Avg Temperature (TAVG):", 5.0, 30.0, 18.0)
        # Historical Rate (Crucial Engineered Feature)
        # In a real app, this would be looked up from a DB, here we take a sample/placeholder
        selected_historical_rate = st.number_input("Historical Operator Delay Rate:", value=0.185, step=0.001)
    
    with col4:
        # Missing Flag (Robustness check)
        selected_missing_flag = st.checkbox("Weather Data Missing?", value=False)
        # Historical Destination Rate
        selected_dest_rate = st.number_input("Historical Destination Delay Rate:", value=0.100, step=0.001)

    submitted = st.form_submit_button("Predict Operational Risk")

# --- 3. Prediction Logic and Output ---

if submitted:
    # 1. Prepare data for the API (must match FlightFeatures Pydantic model in app/main.py)
    input_data = {
        "mes": selected_mes,
        "dianom": selected_dianom,
        "tipovuelo": selected_tipovuelo,
        "opera": selected_opera,
        "siglades": selected_dest,
        "period_day": selected_period,
        "tavg": selected_tavg,
        "opera_historical_delay_rate": selected_historical_rate,
        "dest_historical_delay_rate": selected_dest_rate,
        "tavg_is_missing": 1 if selected_missing_flag else 0
    }
    
    # --- SIMULATION OF FASTAPI CALL ---
    
    # Replace with actual API call in a real deployment
    # API_URL = "http://127.0.0.1:8000/predict"
    # response = requests.post(API_URL, json=input_data)
    # result = response.json()
    
    # --- OFFLINE/MOCK PREDICTION (For testing without running FastAPI) ---
    st.warning("Prediction running in MOCK mode (Offline simulation).")
    
    # Mock Prediction: Higher historical rate -> higher mock probability
    mock_proba = 0.15 + (selected_historical_rate * 2.5) 
    mock_threshold = 0.35
    
    if mock_proba > 0.5:
        mock_proba = 0.5
        
    mock_is_delayed = 1 if mock_proba >= mock_threshold else 0
    
    # --- Display Results (Operational Alert) ---
    
    st.markdown("### 🚨 Prediction Results")
    
    if mock_is_delayed == 1:
        st.error(f"**CRITICAL ALERT:** High Probability of Operational Delay.")
        st.markdown(f"**Recommended Action:** **FLAG** this order/flight for mitigation (e.g., increase ETA buffer, reassign courier, notify supervisor).")
    else:
        st.success("**Status:** On-Time Expected.")
        st.markdown(f"**Recommended Action:** Monitor as Normal.")

    st.markdown("---")
    st.metric("Probability of Delay (> 15 min)", f"{mock_proba:.2%}")
    st.markdown(f"*(Tuned Operational Threshold: {mock_threshold:.2%})*")

# To run: streamlit run app/streamlit_app.py