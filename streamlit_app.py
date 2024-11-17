import streamlit as st
from gtts import gTTS
import tempfile
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="Text-to-Speech App",
    page_icon="🎧",
    layout="wide"
)

# Define languages
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese'
}

def text_to_speech(text, lang='en'):
    """Convert text to speech and return the audio file path"""
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def get_audio_download_link(audio_path, filename="audio.mp3"):
    """Generate a download link for the audio file"""
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio File</a>'
    return href

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main > div {
        padding: 2rem;
    }
    .styled-header {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-align: center;
    }
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.8rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# App Header
st.markdown('<p class="styled-header">🎧 Text-to-Speech Converter</p>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Main input area
    st.subheader("Enter Your Text")
    user_text = st.text_area(
        "Type or paste your text here:",
        height=200,
        placeholder="Enter the text you want to convert to speech..."
    )
    
    # Language selection
    selected_lang = st.selectbox(
        "Select Language",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]
    )
    
    # Generate button with spinner
    if st.button("🔊 Generate Speech", use_container_width=True):
        if user_text.strip():
            with st.spinner("Generating audio... Please wait"):
                audio_file = text_to_speech(user_text, selected_lang)
                
                if audio_file:
                    # Display audio player
                    st.audio(audio_file, format="audio/mp3")
                    
                    # Display download button
                    st.markdown(
                        get_audio_download_link(audio_file, f"speech_{selected_lang}.mp3"),
                        unsafe_allow_html=True
                    )
                    
                    # Add to history
                    st.session_state.history.append({
                        'text': user_text[:100] + '...' if len(user_text) > 100 else user_text,
                        'language': LANGUAGES[selected_lang]
                    })
                    
                    st.success("✅ Audio generated successfully!")
        else:
            st.warning("⚠️ Please enter some text first!")

with col2:
    # History section
    st.subheader("Recent Conversions")
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"Conversion {len(st.session_state.history) - idx}"):
                st.write(f"**Language:** {item['language']}")
                st.write(f"**Text:** {item['text']}")
    else:
        st.info("No conversion history yet")

# Instructions expander
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    1. **Enter Text**: Type or paste your text in the input box
    2. **Select Language**: Choose the desired language from the dropdown
    3. **Generate**: Click the 'Generate Speech' button
    4. **Listen**: Use the audio player to listen to the generated speech
    5. **Download**: Click the download link to save the audio file
    
    **Note**: The audio quality and voice characteristics depend on the selected language.
    """)

# Footer
st.markdown("""
    <div class="footer">
        Created with ❤️ using Streamlit and gTTS
    </div>
    """, unsafe_allow_html=True)
