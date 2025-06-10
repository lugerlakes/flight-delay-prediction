# Streamlit Interface

import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SCL Flight Delay Predictor", layout="centered")
st.title("✈️ Flight Delay Predictor")

st.markdown("Fill in the flight information below to estimate the probability of delay:")

with st.form("flight_form"):
    mes = st.number_input("Month", 1, 12)
    dianom = st.selectbox("Day of the Week", ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
    tipovuelo = st.selectbox("Flight Type", ["N", "I"])
    opera = st.selectbox("Airline", ["Sky Airline", "LATAM Airlines Group", "JetSmart SPA"])
    siglades = st.selectbox("Destination City", ["Antofagasta", "Arica", "Iquique", "Puerto Montt", "Calama", "Concepcion"])
    period_day = st.selectbox("Period of Day", ["morning", "afternoon", "night"])
    high_season = st.radio("Is High Season?", [0, 1])
    is_holiday = st.radio("Is National Holiday?", [0, 1])
    is_strike_day = st.radio("Is Strike Day?", [0, 1])
    tavg = st.number_input("Avg Temperature (°C)", value=15.0)
    tmin = st.number_input("Min Temperature (°C)", value=10.0)
    tmax = st.number_input("Max Temperature (°C)", value=20.0)
    model = st.selectbox("Model", ["logistic_regression", "voting_classifier", "random_forest", "xgboost"])
    
    submitted = st.form_submit_button("Predict Delay")

if submitted:
    input_payload = {
        "mes": mes, "dianom": dianom, "tipovuelo": tipovuelo, "opera": opera, "siglades": siglades,
        "period_day": period_day, "high_season": high_season, "is_holiday": is_holiday,
        "is_strike_day": is_strike_day, "tavg": tavg, "tmin": tmin, "tmax": tmax
    }

    response = requests.post("http://localhost:8000/predict", json=input_payload, params={"model_name": model})

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Delay Probability: {result['delay_probability']:.2%}")
        st.info(f"Predicted Class: {'DELAY' if result['predicted_class'] == 1 else 'ON TIME'}")
        st.caption(f"Model Used: {result['model_used']}")
    else:
        st.error("Failed to get prediction. Check inputs or try again later.")
