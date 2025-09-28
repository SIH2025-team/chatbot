import streamlit as st
import pandas as pd
import plotly.express as px

st.title("EcoMeter (Personal Carbon Footprint Tracker) 🚗")
st.write("This page helps you estimate the carbon emissions of your daily commute.")

# Mock dataset for carbon emissions per km (in kg CO2)
emission_factors = {
    "Car": 0.20,
    "Bus": 0.05,
    "Bike": 0.0,
    "Walk": 0.0
}

# Add a form for user input
with st.form(key='emissions_form'):
    distance = st.slider("Distance traveled (in km)", min_value=1, max_value=100, value=10)
    vehicle = st.selectbox("Vehicle Type", list(emission_factors.keys()))
    submit_button = st.form_submit_button(label='Calculate Emissions')

if submit_button:
    # Calculate emissions and create a DataFrame for visualization
    calculated_emission = distance * emission_factors[vehicle]
    
    # Create a DataFrame for the bar chart
    data = {
        'Vehicle': list(emission_factors.keys()),
        'CO2 Emissions (kg)': [distance * e for e in emission_factors.values()]
    }
    df = pd.DataFrame(data)
    
    st.markdown("---")
    st.subheader(f"Your Emissions: {calculated_emission:.2f} kg CO2")

    # Create a bar chart comparing emissions
    fig = px.bar(
        df,
        x='Vehicle',
        y='CO2 Emissions (kg)',
        title=f"Comparison of Emissions for a {distance} km commute",
        color='CO2 Emissions (kg)',
        color_continuous_scale=px.colors.sequential.YlGn
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"Your commute with a **{vehicle}** produced approximately **{calculated_emission:.2f} kg of CO2**. 😊")