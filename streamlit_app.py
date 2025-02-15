import streamlit as st
from TTS.api import TTS
import os
from pydub import AudioSegment
from io import BytesIO
import soundfile as sf
import numpy as np

# Cache the TTS model to improve efficiency.
@st.cache_resource
def load_tts(model_name):
    return TTS(model_name=model_name, progress_bar=False, gpu=False)

def change_speed(sound, speed=1.0):
    """
    Adjust the speed of an AudioSegment by modifying its frame rate.
    """
    altered = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return altered.set_frame_rate(sound.frame_rate)

# Define available voice models (each model represents a distinct voice style)
VOICE_MODELS = {
    "LJSpeech (Female, US) - Tacotron2-DDC": "tts_models/en/ljspeech/tacotron2-DDC",
    "VCTK (Male, UK) - VITS": "tts_models/en/vctk/vits"
}

# Configure the Streamlit page
st.set_page_config(page_title="Coqui TTS Converter", layout="centered")
st.title("🎤 Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# Sidebar: Voice model selection and speech speed adjustment
st.sidebar.header("Voice Settings")
voice_choice = st.sidebar.selectbox("Select Voice Model:", list(VOICE_MODELS.keys()), index=0)
speed = st.sidebar.slider("Speech Speed", min_value=0.8, max_value=1.2, value=1.0, step=0.05)

# Main text input
user_input = st.text_area("Enter text to convert to speech:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Load the selected TTS model (using caching)
        model_name = VOICE_MODELS[voice_choice]
        tts_model = load_tts(model_name)
        
        # Define output file path
        output_path = "output.wav"
        
        # Generate speech and save to file
        tts_model.tts_to_file(text=user_input, file_path=output_path)
        
        # If speed adjustment is needed, use pydub to modify playback speed
        if speed != 1.0:
            sound = AudioSegment.from_wav(output_path)
            adjusted_sound = change_speed(sound, speed)
            adjusted_output = "output_adjusted.wav"
            adjusted_sound.export(adjusted_output, format="wav")
            output_path = adjusted_output
        
        st.audio(output_path, format="audio/wav")
        
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        st.download_button("Download Audio", audio_bytes, file_name=os.path.basename(output_path), mime="audio/wav")
        
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")
