import streamlit as st
from TTS.api import TTS
import soundfile as sf
import os

# Configure the Streamlit page
st.set_page_config(page_title="Coqui TTS Converter", layout="centered")
st.title("🎤 Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# Text input for conversion
user_input = st.text_area("Enter text to convert to speech:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Initialize the TTS model (using a pre-trained model from Coqui TTS)
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
        
        # Define output file path
        output_path = "output.wav"
        
        # Generate speech and save to output file
        tts.tts_to_file(text=user_input, file_path=output_path)
        
        # Display the audio in the app
        st.audio(output_path, format="audio/wav")
        
        # Provide a download button for the audio file
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        st.download_button("Download Audio", audio_bytes, file_name="output.wav", mime="audio/wav")
        
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")
