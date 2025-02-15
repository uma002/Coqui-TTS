import streamlit as st
from TTS.api import TTS
import os

# Define available voice models
VOICE_MODELS = {
    "LJSpeech (US Female) - Tacotron2-DDC": "tts_models/en/ljspeech/tacotron2-DDC",
    "VCTK (UK Male) - VITS": "tts_models/en/vctk/vits"
}

st.set_page_config(page_title="Simple Coqui TTS App", layout="centered")
st.title("Simple Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# Sidebar: Available pre-trained models using a select slider
st.sidebar.header("Voice Settings")
voice_choice = st.sidebar.select_slider(
    "Select Voice Model:",
    options=list(VOICE_MODELS.keys()),
    value="LJSpeech (US Female) - Tacotron2-DDC"
)

# Main text input
user_input = st.text_area("Enter text:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Load the selected TTS model
        model_name = VOICE_MODELS[voice_choice]
        tts_model = TTS(model_name=model_name, progress_bar=False, gpu=False)
        
        output_path = "output.wav"
        # Generate speech and save to output file
        tts_model.tts_to_file(text=user_input, file_path=output_path)
        
        # Display the audio in the app
        st.audio(output_path, format="audio/wav")
        
        # Provide a download button for the audio file
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        st.download_button("Download Audio", audio_bytes, file_name="output.wav", mime="audio/wav")
        
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")
