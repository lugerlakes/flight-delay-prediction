# streamlit_app.py — Airline Flight Delay Prediction Interface

import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "https://lugerlakes--flight-delay-api-run-api-dev.modal.run")

# Page config
st.set_page_config(page_title="SCL Flight Delay Predictor", layout="centered")
st.title("✈️ SCL Flight Delay Predictor ✈️")
st.markdown(
    "This tool helps **airline operations personnel** predict the risk of flight delays based on flight attributes and weather conditions."
)

# Input form
with st.form("flight_form"):
    st.subheader("📋 Flight Information")

    col1, col2 = st.columns(2)
    with col1:
        mes = st.number_input("Month", 1, 12, step=1)
        dianom = st.selectbox("Day of the Week", ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
        tipovuelo = st.selectbox("Flight Type", ["N", "I"])
        period_day = st.selectbox("Period of Day", ["morning", "afternoon", "night"])
    with col2:
        opera = st.selectbox("Airline", ["Sky Airline", "LATAM Airlines Group", "JetSmart SPA"])
        siglades = st.selectbox("Destination City", ["Antofagasta", "Arica", "Iquique", "Puerto Montt", "Calama", "Concepcion"])
        high_season = st.radio("High Season?", [0, 1], horizontal=True)
        is_holiday = st.radio("Holiday?", [0, 1], horizontal=True)
        is_strike_day = st.radio("Strike Day?", [0, 1], horizontal=True)

    st.subheader("🌡️ Weather Conditions at Departure")
    tavg = st.number_input("Avg Temperature (°C)", value=15.0)
    tmin = st.number_input("Min Temperature (°C)", value=10.0)
    tmax = st.number_input("Max Temperature (°C)", value=20.0)

    st.subheader("🧠 Model Selection")
    model = st.selectbox("Choose a model", ["logistic_regression", "voting_classifier", "random_forest", "xgboost"])

    submitted = st.form_submit_button("🚀 Predict Delay")

# Submit request
if submitted:
    input_payload = {
        "mes": mes,
        "dianom": dianom,
        "tipovuelo": tipovuelo,
        "opera": opera,
        "siglades": siglades,
        "period_day": period_day,
        "high_season": high_season,
        "is_holiday": is_holiday,
        "is_strike_day": is_strike_day,
        "tavg": tavg,
        "tmin": tmin,
        "tmax": tmax
    }

    with st.spinner("⏳ Contacting prediction engine..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=input_payload, params={"model_name": model})
            response.raise_for_status()
            result = response.json()

            st.success(f"🎯 Predicted Delay Probability: {result['delay_probability']:.2%}")
            st.info(f"🛬 Predicted Class: {'✈️ DELAY' if result['predicted_class'] == 1 else '✅ ON TIME'}")
            st.caption(f"Model Used: `{result['model_used']}`")

            st.markdown("### 📊 Raw Input Sent to API")
            st.json(input_payload)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
