import streamlit as st
import pandas as pd
import plotly.express as px
import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator
import re

# Function to load the data from the CSV file
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), '../data/groundwater_india_2024_complete.csv')
    df = pd.read_csv(file_path)
    return df

# CHANGED: New dynamic function to find data at state OR district level
def get_data_from_query(query_text, df):
    query_text = query_text.lower()
    
    indian_states_and_uts = [
        'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chhattisgarh', 'goa', 'gujarat', 
        'haryana', 'himachal pradesh', 'jharkhand', 'karnataka', 'kerala', 'madhya pradesh', 
        'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'punjab', 
        'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 
        'uttarakhand', 'west bengal', 'andaman and nicobar islands', 'chandigarh', 
        'dadra and nagar haveli and daman and diu', 'delhi', 'jammu and kashmir', 
        'ladakh', 'lakshadweep', 'puducherry'
    ]
    
    # Step 1: Check for a state in the query
    found_state = None
    for state in indian_states_and_uts:
        if state in query_text:
            found_state = state
            break

    found_year = None
    year_match = re.search(r'\b\d{4}\b', query_text)
    if year_match:
        found_year = int(year_match.group(0))

    if found_state:
        # Filter for state-level data
        state_level_df = df[df['Level'].str.lower() == 'state/ut']
        filtered_df = state_level_df[state_level_df['State/UT'].str.lower() == found_state]
        if found_year:
            filtered_df = filtered_df[filtered_df['Year'] == found_year]
        
        if not filtered_df.empty:
            return filtered_df
    
    # Step 2: If no state found, check for a district in the query
    # This is a fallback to search for any keyword in the District/Block column
    district_level_df = df[df['Level'].str.lower() == 'district/block']
    
    if query_text:
        # Check if any word in the query matches a district name
        query_words = query_text.split()
        for word in query_words:
            matching_districts = district_level_df[district_level_df['District/Block'].str.lower().str.contains(word)]
            if not matching_districts.empty:
                filtered_df = matching_districts
                # Further filter by year if found
                if found_year:
                    filtered_df = filtered_df[filtered_df['Year'] == found_year]
                return filtered_df
            
    return pd.DataFrame()

# CHANGED: Function to generate a plot
def create_chart(df):
    if df.empty:
        return None

    # NEW: Determine if the data is state or district level
    if 'State/UT' in df.columns:
        name = df['State/UT'].iloc[0]
        y_axis_label = "Groundwater Stage of Development (%)"
        title = f'{name}: Groundwater Stage of Development'
        y_column = 'Stage (%)'
    else:
        name = df['District/Block'].iloc[0]
        y_axis_label = "Groundwater Stage of Development (%)"
        title = f'{name}: Groundwater Stage of Development'
        y_column = 'Stage (%)'
    
    fig = px.line(df, x='Year', y=y_column, 
                  title=title,
                  markers=True)
    fig.update_traces(marker_size=10)
    fig.update_layout(yaxis_title=y_axis_label)
    
    return fig

# --- Voice & Translation Functions (No change here) ---

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    try:
        query = r.recognize_google(audio, language="en-IN")
        st.success("Recognized: " + query)
        return query
    except sr.UnknownValueError:
        st.warning("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return ""

def text_to_speech(text, lang='en'):
    tts = gTTS(text, lang=lang)
    audio_path = "temp_response.mp3"
    tts.save(audio_path)
    
    try:
        sound = AudioSegment.from_mp3(audio_path)
        play(sound)
    except Exception as e:
        st.warning(f"Audio playback failed: {e}")
    
    st.audio(audio_path, format="audio/mpeg", start_time=0)
    
    os.remove(audio_path)

def translate_text(text, dest_lang='en'):
    translator = Translator()
    return translator.translate(text, dest=dest_lang).text