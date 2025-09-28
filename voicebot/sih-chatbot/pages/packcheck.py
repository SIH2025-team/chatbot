import streamlit as st
st.title("PackCheck (Plastic Packaging Impact Analyzer)")
st.write("This page will analyze the environmental impact of plastic packaging.")

st.header("Packaging Material Breakdown")
material = st.selectbox("Select Material", ["Plastic (PET)", "Glass", "Aluminum", "Paper"])
if material == "Plastic (PET)":
    st.write("PET plastic is recyclable, but its production is energy-intensive.")
elif material == "Aluminum":
    st.write("Aluminum is highly recyclable and efficient to recycle, but requires a lot of energy to produce.")
else:
    st.write("Good choice! These materials have a lower environmental impact.")