import streamlit as st
import torch
import numpy as np
import soundfile as sf
from TTS.api import TTS

# Load TTS model (ensure you have a supported model installed)
MODEL_NAME = "tts_models/en/ljspeech/tacotron2-DDC"
tts = TTS(MODEL_NAME).to("cpu" if not torch.cuda.is_available() else "cuda")

# Streamlit App UI
st.title("Text-to-Speech Converter (Coqui TTS)")

# Sidebar settings
st.sidebar.header("Settings")
selected_voice = st.sidebar.selectbox("Select Voice", ["LJSpeech (Default)"])
speed = st.sidebar.slider("Speed", 0.5, 1.5, 1.0)  # Adjust speech speed

# User input text
user_input = st.text_area("Enter text to convert to speech:", "")

if st.button("Convert to Speech"):
    if user_input:
        # Generate speech
        output_wav = "output.wav"
        tts.tts_to_file(text=user_input, file_path=output_wav, speed=speed)

        # Load and play the generated audio
        audio_data, samplerate = sf.read(output_wav)
        st.audio(audio_data, format="audio/wav", sample_rate=samplerate)
    else:
        st.warning("Please enter text before converting.")

