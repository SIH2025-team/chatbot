import streamlit as st
st.title("EcoMeter (Personal Carbon Footprint Tracker)")
st.write("This page will help you track your personal carbon footprint.")

st.header("Daily Commute Emissions")
distance = st.slider("Distance traveled (km)", min_value=1, max_value=100, value=10)
vehicle = st.selectbox("Vehicle Type", ["Car", "Bus", "Bike", "Walk"])
if vehicle == "Car":
    st.write(f"Your estimated carbon emissions are {distance * 0.1} kg CO2.")
else:
    st.write("Your commute is eco-friendly! 😊")