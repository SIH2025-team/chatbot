import streamlit as st
import pandas as pd
import plotly.express as px

st.title("PackCheck (Plastic Packaging Impact Analyzer) ♻️")
st.write("This page helps you compare the environmental impact of different packaging materials.")

# Mock dataset for environmental impact (Embodied Energy in MJ/kg, Recyclability score 1-10)
material_impact = {
    "Material": ["Plastic (PET)", "Glass", "Aluminum", "Paper"],
    "Embodied Energy (MJ/kg)": [80, 15, 170, 10],
    "Recyclability Score": [8, 5, 10, 7]
}
df_impact = pd.DataFrame(material_impact)
df_impact.set_index("Material", inplace=True)

# Add an interactive element (Dropdown) to select the metric
metric_options = ["Embodied Energy (MJ/kg)", "Recyclability Score"]
selected_metric = st.selectbox("Select a Metric to Compare", metric_options)

st.markdown("---")
st.subheader(f"Comparison by {selected_metric}")

# Create a bar chart based on the selected metric
fig = px.bar(
    df_impact,
    x=df_impact.index,
    y=selected_metric,
    title=f"Environmental Impact of Materials: {selected_metric}",
    color=selected_metric,
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Key Insights")
if selected_metric == "Embodied Energy (MJ/kg)":
    st.info("💡 **Insight:** Aluminum packaging requires the most energy to produce, while paper is the most energy-efficient.")
else:
    st.info("💡 **Insight:** Aluminum is the most recyclable material, but all materials shown here have high recyclability.")