import streamlit as st
from TTS.api import TTS
import os
import soundfile as sf

# Configure the Streamlit page
st.set_page_config(page_title="Coqui TTS Converter", layout="centered")
st.title("🎤 Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# User input text
user_input = st.text_area("Enter text to convert to speech:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Initialize the TTS model
        # This example uses the pre-trained model "tts_models/en/ljspeech/tacotron2-DDC"
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
        
        # Define the output file path
        output_path = "output.wav"
        
        # Generate speech and save to file
        tts.tts_to_file(text=user_input, file_path=output_path)
        
        # Play the generated audio in the app
        st.audio(output_path, format="audio/wav")
        
        # Provide a download button for the audio file
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        st.download_button("Download Audio", audio_bytes, file_name="output.wav", mime="audio/wav")
        
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")
