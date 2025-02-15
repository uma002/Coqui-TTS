import streamlit as st
from TTS.api import TTS
import os

st.set_page_config(page_title="Simple Coqui TTS App", layout="centered")
st.title("Simple Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# Main text input
user_input = st.text_area("Enter text:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Use the LJSpeech model (female voice) which does not require espeak
        tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
        
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
