import streamlit as st

# The set_page_config should be in the main app file only
st.set_page_config(
    page_title="JalMitra ChatBot",
    page_icon="💧",
    layout="wide"
)

# Use st.session_state to store the user's name
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Check if the user's name is in session state
if st.session_state.user_name:
    # If the name is already there, display the personalized welcome
    st.title(f"Welcome, {st.session_state.user_name}! 👋")
    st.write("You are on the Home page.")
    st.write("Use the sidebar on the left to navigate to different sections.")
    
    # Optional: Add a button to reset the name
    if st.button("Change Name"):
        st.session_state.user_name = None
        st.rerun()

else:
    # If the name is not in session state, ask for it
    st.title("Welcome to JalMitra💧 Chatbot!")
    
    # Use st.text_input with a key to check for changes
    user_name_input = st.text_input("Please enter your name:", key="name_input")
    
    if user_name_input:
        st.session_state.user_name = user_name_input
        st.rerun()