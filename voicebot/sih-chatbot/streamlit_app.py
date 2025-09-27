import streamlit as st
import pandas as pd
from utils.helper import load_data, get_data_from_query, create_chart, recognize_speech, text_to_speech, translate_text

# --- Page Configuration ---
st.set_page_config(
    page_title="JalMitra",
    page_icon="💧",
    layout="wide"
)

# --- Load Data (cached to avoid reloading) ---
groundwater_df = load_data()

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Language Selection and Title ---
col1, col2 = st.columns([1, 4])
with col1:
    language = st.radio("Language", ["English", "Hindi"], horizontal=True, index=0)
    lang_code = 'hi' if language == 'Hindi' else 'en'
    
with col2:
    st.title("JalMitra")
    
if lang_code == 'hi':
    st.markdown("भूजल डेटा को सरल और सुलभ बनाएं।")
else:
    st.markdown("Making Groundwater Data Simple and Accessible.")

# --- Display Chat Messages from History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "summary" in message:
            st.markdown(f"**Summary:** {message['summary']}")
        if not message["table"].empty:
            st.dataframe(message["table"], use_container_width=True)
        if message["chart"]:
            st.plotly_chart(message["chart"], use_container_width=True)

# --- Handle User Input ---
# Use a button to trigger voice input
voice_button = st.button("🎤 Speak Your Query")
user_query = ""

if voice_button:
    user_query = recognize_speech()

if user_query or (user_query := st.chat_input("Ask a question about groundwater data...")):
    # If the language is Hindi, translate the query to English for processing
    if lang_code == 'hi' and user_query:
        # We assume the user speaks Hindi, so the source is 'hi'
        user_query_en = translate_text(user_query, dest_lang='en')
        st.session_state.messages.append({"role": "user", "content": f"🗣️ **(Hindi):** {user_query}"})
        st.session_state.messages.append({"role": "user", "content": f"📝 **(Translated):** {user_query_en}"})
        # The internal query will be the English version
        internal_query = user_query_en
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        internal_query = user_query
    
    with st.chat_message("user"):
        st.write(user_query)
        
    # Get the data from the helper function using the internal query
    response_df = get_data_from_query(internal_query, groundwater_df)
    
    # Generate the chart
    chart_figure = create_chart(response_df)
    
    # Create the summary text based on the data
    if not response_df.empty:
        district = response_df['District'].iloc[0]
        groundwater_level = response_df['Groundwater_Level'].iloc[0]
        summary_text = f"The average groundwater level for {district} in 2020 was {groundwater_level}."
        
        if lang_code == 'hi':
            summary_text_hi = translate_text(summary_text, dest_lang='hi')
            summary_text = summary_text_hi
    else:
        summary_text = "Sorry, I could not find data for that query. Please try 'Pune 2020' or 'Compare Delhi'."
        if lang_code == 'hi':
            summary_text = "क्षमा करें, मुझे इस प्रश्न का डेटा नहीं मिल सका। कृपया 'पुणे 2020' या 'दिल्ली की तुलना करें' जैसा कुछ प्रयास करें।"
    
    # Convert the summary to speech and play it
    text_to_speech(summary_text, lang=lang_code)
    
    # Create the assistant's response dictionary
    assistant_response = {
        "role": "assistant",
        "content": "Here are the results:",
        "summary": summary_text,
        "table": response_df,
        "chart": chart_figure
    }
    
    # Add assistant response to the chat history
    st.session_state.messages.append(assistant_response)
    
    # Display the new assistant message in the chat UI
    with st.chat_message("assistant"):
        st.write("Here are the results:")
        st.markdown(f"**Summary:** {summary_text}")
        if not response_df.empty:
            st.dataframe(response_df, use_container_width=True)
        if chart_figure:
            st.plotly_chart(chart_figure, use_container_width=True)


# Here is a video from YouTube about the development of a real-time speech-to-text application with Streamlit. This video is relevant as it provides a practical example of implementing a speech-to-text feature in a Streamlit application, which is a core component of your project.
