import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Function to load the data from the CSV file
@st.cache_data
def load_data_for_reports():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'groundwater_india_2024_complete.csv')
    df = pd.read_csv(file_path)
    return df

st.title("Reports & Insights")
st.write("This page provides a high-level overview of India's groundwater data.")

# Load the complete dataset
groundwater_df = load_data_for_reports()

# Filter for only state-level data
state_level_df = groundwater_df[groundwater_df['Level'] == 'State/UT'].copy()

# Ensure numeric types and handle spaces in column names
state_level_df['Stage (%)'] = pd.to_numeric(state_level_df['Stage (%)'])
state_level_df['Recharge (ham)'] = pd.to_numeric(state_level_df['Recharge (ham)'])
state_level_df['Extraction (ham)'] = pd.to_numeric(state_level_df['Extraction (ham)'])
state_level_df['Status'] = state_level_df['Status'].astype('category')


# Add an interactive element (Dropdown) to select the metric
metric_options = {
    "Stage of Development (%)": 'Stage (%)',
    "Total Recharge (ham)": 'Recharge (ham)',
    "Total Extraction (ham)": 'Extraction (ham)',
}
selected_metric_name = st.selectbox("Select a Metric to View", list(metric_options.keys()))
selected_metric_column = metric_options[selected_metric_name]

# Generate the dynamic bar chart
fig = px.bar(
    state_level_df.sort_values(by=selected_metric_column, ascending=False),
    x='State/UT',
    y=selected_metric_column,
    title=f'Groundwater {selected_metric_name} by State/UT',
    color='Status', # Use 'Status' to color the bars for visual insight
    color_discrete_map={
        'Over-Exploited': 'red',
        'Critical': 'orange',
        'Semi-Critical': 'yellow',
        'Safe': 'green'
    }
)

st.plotly_chart(fig, use_container_width=True)


# Add an insight summary
st.markdown("### Key Insights")
over_exploited_states = state_level_df[state_level_df['Status'] == 'Over-Exploited']['State/UT'].tolist()
semi_critical_states = state_level_df[state_level_df['Status'] == 'Semi-Critical']['State/UT'].tolist()

if over_exploited_states:
    st.warning(f"⚠️ **Urgent Concern:** The following states have been classified as **Over-Exploited**: {', '.join(over_exploited_states)}.")

if semi_critical_states:
    st.info(f"💡 **Action Needed:** The following states are in a **Semi-Critical** condition: {', '.join(semi_critical_states)}.")

safe_states_count = state_level_df[state_level_df['Status'] == 'Safe'].shape[0]
total_states_count = state_level_df.shape[0]
st.success(f"✅ **Good News:** {safe_states_count} out of {total_states_count} states are currently in the **Safe** zone.")