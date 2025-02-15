import streamlit as st
from TTS.api import TTS
from pydub import AudioSegment
from io import BytesIO
import os

# Cache the TTS model to improve efficiency.
@st.cache_resource(show_spinner=False)
def load_tts(model_name):
    return TTS(model_name=model_name, progress_bar=False, gpu=False)

def adjust_speed(audio_path, speed):
    """
    Adjust the speed of the audio using pydub.
    Returns a BytesIO buffer containing the adjusted WAV audio.
    """
    sound = AudioSegment.from_file(audio_path, format="wav")
    # Change the frame rate to adjust speed.
    new_frame_rate = int(sound.frame_rate * speed)
    altered_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate})
    # To keep compatibility, set the frame rate back to original.
    adjusted_sound = altered_sound.set_frame_rate(sound.frame_rate)
    buffer = BytesIO()
    adjusted_sound.export(buffer, format="wav")
    buffer.seek(0)
    return buffer

# Define available voice models (each model represents a distinct voice style)
VOICE_MODELS = {
    "LJSpeech (US Female) - Tacotron2-DDC": "tts_models/en/ljspeech/tacotron2-DDC",
    "VCTK (UK Male) - VITS": "tts_models/en/vctk/vits"
}

# Configure the Streamlit page
st.set_page_config(page_title="Coqui TTS Converter", layout="centered")
st.title("🎤 Coqui TTS Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech using Coqui TTS.")

# Sidebar for voice settings and speed adjustment
st.sidebar.header("Voice Settings")
voice_choice = st.sidebar.selectbox("Select Voice Model:", list(VOICE_MODELS.keys()), index=0)
speed = st.sidebar.slider("Speech Speed", min_value=0.8, max_value=1.2, value=1.0, step=0.05)

# Main text input
user_input = st.text_area("Enter text to convert to speech:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Load the selected TTS model (cached)
        model_name = VOICE_MODELS[voice_choice]
        tts_model = load_tts(model_name)
        
        output_path = "output.wav"
        # Generate speech and save to output file
        tts_model.tts_to_file(text=user_input, file_path=output_path)
        
        # If speed is not normal, adjust the audio
        if speed != 1.0:
            audio_buffer = adjust_speed(output_path, speed)
            # Optionally, save the adjusted audio to a file for playback
            adjusted_path = "output_adjusted.wav"
            with open(adjusted_path, "wb") as f:
                f.write(audio_buffer.read())
            final_audio = adjusted_path
        else:
            final_audio = output_path
        
        st.audio(final_audio, format="audio/wav")
        
        with open(final_audio, "rb") as f:
            audio_bytes = f.read()
        st.download_button("Download Audio", audio_bytes, file_name=os.path.basename(final_audio), mime="audio/wav")
        
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")
