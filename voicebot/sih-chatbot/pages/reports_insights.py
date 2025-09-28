import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Reports & Insights")
st.write("This page shows a high-level overview of our groundwater data.")

# Create a mock report chart
report_data = pd.DataFrame({
    'District': ['Pune', 'Nagpur', 'Delhi'],
    'Groundwater_Level_2021': [42, 53, 28]
})

fig = px.bar(report_data, x='District', y='Groundwater_Level_2021',
             title='Groundwater Levels in 2021 by District',
             color='District')
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Key Findings")
st.info("Pune and Nagpur show relatively healthy groundwater levels compared to Delhi.")