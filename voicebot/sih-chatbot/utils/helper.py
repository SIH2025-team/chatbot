import streamlit as st
import pandas as pd
import plotly.express as px
import os
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator

# Function to load the data from the CSV file
@st.cache_data
def load_data():
    # Use os.path.join to create a path that works on any OS
    file_path = os.path.join(os.path.dirname(__file__), '../data/groundwater.csv')
    df = pd.read_csv(file_path)
    return df

# Function to find data for a specific query
def get_data_from_query(query_text, df):
    query_text = query_text.lower()
    
    if "pune" in query_text:
        return df[df['District'].str.lower() == 'pune']
    elif "delhi" in query_text:
        return df[df['District'].str.lower() == 'delhi']
    elif "nagpur" in query_text:
        return df[df['District'].str.lower() == 'nagpur']

    return pd.DataFrame()

# Function to generate a plot
def create_chart(df):
    if df.empty:
        return None

    # Determine the title based on the district(s) in the DataFrame
    district_name = df['District'].iloc[0]
    
    # Create a line chart showing the trend over years
    fig = px.line(df, x='Year', y='Groundwater_Level', 
                  title=f'{district_name}: Groundwater Level Trend',
                  markers=True)
    fig.update_traces(marker_size=10)
    fig.update_layout(yaxis_title="Groundwater Level")
    
    return fig

# --- Voice & Translation Functions ---

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    try:
        query = r.recognize_google(audio, language="en-IN") # You can specify language here
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
    
    # Use pydub to play the audio file (requires FFmpeg)
    # This might not work on all cloud deployments without FFmpeg installed
    try:
        sound = AudioSegment.from_mp3(audio_path)
        play(sound)
    except Exception as e:
        st.warning(f"Audio playback failed: {e}")
    
    # You can also use st.audio() to embed a player in the UI
    st.audio(audio_path, format="audio/mpeg", start_time=0)
    
    # Clean up the temporary file
    os.remove(audio_path)

def translate_text(text, dest_lang='en'):
    translator = Translator()
    return translator.translate(text, dest=dest_lang).text