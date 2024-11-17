import streamlit as st
from gtts import gTTS
import os
import tempfile

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    # Create a temporary file to store the audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False)
    tts.save(temp_audio.name)
    return temp_audio.name

# Streamlit App
def main():
    st.title("Text-to-Speech Generator")
    
    # Text input from the user
    user_text = st.text_area("Enter the text you want to convert to speech:", "Hello, welcome to the text-to-speech generator!")
    
    if st.button("Convert to Speech"):
        if user_text.strip() != "":
            audio_file = text_to_speech(user_text)
            st.audio(audio_file, format="audio/mp3")
            st.success("Audio generated successfully!")
        else:
            st.error("Please enter some text to convert to speech.")
    
if __name__ == "__main__":
    main()
