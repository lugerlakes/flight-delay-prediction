import streamlit as st
import requests
import json
import os

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="SCL Airport Operations", layout="centered", page_icon="🛫")

# --- UI Header ---
st.title("🛫 Flight Delay Risk Command Center")
st.markdown("""
**Objective:** Proactive detection of flights at risk of delay (>15 min).
**Champion Model:** **XGBoost Classifier** (Selected for 78% Recall vs 59% of Ensemble).
""")
st.markdown("---")

# --- Input Form ---
with st.form("prediction_form"):
    st.subheader("1. Flight Information")
    col1, col2 = st.columns(2)
    
    with col1:
        operating_airline = st.selectbox(
            "Operating Airline", 
            ['Latin American Wings', 'Grupo LATAM', 'Sky Airline', 'Copa Air', 'American Airlines', 'Others']
        )
        destination_city_name = st.selectbox(
            "Destination City",
            ['Buenos Aires', 'Miami', 'Lima', 'Sao Paulo', 'Santiago', 'Antofagasta']
        )
        flight_type = st.radio("Flight Type", ['I', 'N'])

    with col2:
        month = st.slider("Month", 1, 12, 1)
        day_of_week_name = st.selectbox(
            "Day of Week",
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )
        period_day = st.select_slider(
            "Time of Day",
            options=['morning', 'afternoon', 'night']
        )

    st.subheader("2. Operational & Environmental Context")
    col3, col4 = st.columns(2)
    
    with col3:
        wspd = st.number_input("Wind Speed (knots)", min_value=0.0, value=5.0)
        pres = st.number_input("Atmospheric Pressure (hPa)", min_value=900.0, value=1013.0)
    
    with col4:
        opera_risk = st.slider("Airline Hist. Delay Rate", 0.0, 1.0, 0.18)
        dest_risk = st.slider("Dest. Hist. Delay Rate", 0.0, 1.0, 0.15)

    st.caption("Advanced: Simulate missing weather data?")
    weather_missing = st.checkbox("Weather API Down (Simulate Missing)", value=False)

    submit_btn = st.form_submit_button("🚨 Calculate Risk (XGBoost)")

# --- Logic ---
if submit_btn:
    payload = {
        "operating_airline": operating_airline,
        "destination_city_name": destination_city_name,
        "period_day": period_day,
        "day_of_week_name": day_of_week_name,
        "flight_type": flight_type,
        "month": month,
        "wspd": -999 if weather_missing else wspd,
        "pres": -999 if weather_missing else pres,
        "opera_historical_delay_rate": opera_risk,
        "dest_historical_delay_rate": dest_risk,
        "wspd_is_missing": 1 if weather_missing else 0,
        "pres_is_missing": 1 if weather_missing else 0
    }

    try:
        with st.spinner("Querying XGBoost Engine..."):
            response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            score = result['confidence_score']
            is_delay = result['prediction'] == 'DELAY'
            
            st.markdown("### Prediction Results")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Delay Probability", f"{score:.1%}")
            with col2:
                if is_delay:
                    st.error(f"⚠️ **HIGH RISK DETECTED**")
                    st.write(f"Probability exceeds operational threshold of {result['threshold_used']}.")
                else:
                    st.success(f"✅ **Low Risk**")
                    st.write("Operations expected to be normal.")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Connection Error: Is the API running?")