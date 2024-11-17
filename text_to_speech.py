import streamlit as st
from gtts import gTTS
from googletrans import Translator
import os
import tempfile
import base64
from datetime import datetime
import json

# Load language codes and names
def load_languages():
    return {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
        'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi'
    }

# Function to get download link
def get_download_link(audio_path, filename):
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio File</a>'
    return href

# Function to translate text
def translate_text(text, target_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Function to convert text to speech with enhanced options
def text_to_speech(text, lang='en', speed=1.0):
    try:
        tts = gTTS(text=text, lang=lang, slow=(speed < 1.0))
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_audio.name)
        return temp_audio.name
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None

# Function to save history
def save_history(text, lang, timestamp):
    history = []
    if os.path.exists('tts_history.json'):
        with open('tts_history.json', 'r') as f:
            history = json.load(f)
    
    history.append({
        'text': text,
        'language': lang,
        'timestamp': timestamp
    })
    
    with open('tts_history.json', 'w') as f:
        json.dump(history[-10:], f)  # Keep only last 10 entries

# Main Streamlit app
def main():
    st.set_page_config(page_title="Advanced Text-to-Speech Generator", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            width: 100%;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎧 Advanced Text-to-Speech Generator")
    
    # Sidebar controls
    st.sidebar.header("Settings")
    languages = load_languages()
    selected_lang = st.sidebar.selectbox("Select Language", 
                                       options=list(languages.keys()),
                                       format_func=lambda x: languages[x])
    
    speed = st.sidebar.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Text")
        user_text = st.text_area(
            "Enter the text you want to convert to speech:",
            height=200,
            placeholder="Type or paste your text here..."
        )
        
        # Word count
        if user_text:
            word_count = len(user_text.split())
            st.info(f"Word count: {word_count}")
    
    with col2:
        st.subheader("Recent History")
        if os.path.exists('tts_history.json'):
            with open('tts_history.json', 'r') as f:
                history = json.load(f)
                for entry in reversed(history):
                    with st.expander(f"{entry['timestamp']} - {languages[entry['language']]}"):
                        st.write(entry['text'][:100] + "..." if len(entry['text']) > 100 else entry['text'])

    # Process and generate audio
    if st.button("🔊 Generate Speech"):
        if user_text.strip() != "":
            with st.spinner("Processing..."):
                # Translate if necessary
                if selected_lang != 'en':
                    user_text = translate_text(user_text, selected_lang)
                
                # Generate audio
                audio_file = text_to_speech(user_text, selected_lang, speed)
                
                if audio_file:
                    # Display audio player
                    st.audio(audio_file, format="audio/mp3")
                    
                    # Generate download link
                    filename = f"tts_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                    st.markdown(get_download_link(audio_file, filename), unsafe_allow_html=True)
                    
                    # Save to history
                    save_history(user_text, selected_lang, 
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                    st.success("✅ Audio generated successfully!")
        else:
            st.error("⚠️ Please enter some text to convert to speech.")

    # Display instructions
    with st.expander("How to Use"):
        st.markdown("""
        1. Enter your text in the input area
        2. Select your desired language from the sidebar
        3. Adjust the speech speed if needed
        4. Click 'Generate Speech' to create the audio
        5. Use the audio player to listen or download the file
        6. View your recent conversions in the history panel
        """)

if __name__ == "__main__":
    main()
