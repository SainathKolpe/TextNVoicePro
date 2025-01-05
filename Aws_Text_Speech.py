import streamlit as st
from gtts import gTTS
from googletrans import Translator
import os

# Streamlit UI - Title and Subtitle
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>🌟 Text Processing Tool 🌟</h1>
    <h3 style='text-align: center; color: #555;'>Welcome to the Text Processing Tool! Convert text to speech or translate it into different languages.</h3>
""", unsafe_allow_html=True)

# Language selection dropdown for user
language = st.selectbox("Select your input language:", ["English", "Hindi", "Marathi"])

# Text input box for user to enter text
text_input = st.text_area(f"Enter text in {language}:", height=150)

# Reset session state when text input changes
if 'prev_text' not in st.session_state:
    st.session_state.prev_text = ""

if text_input != st.session_state.prev_text:
    st.session_state.prev_text = text_input
    st.session_state.translated_text = ""
    st.session_state.translate_action = False

# Initialize session state for managing translation and speech generation
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'translate_action' not in st.session_state:
    st.session_state.translate_action = False
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = ""

# Action selection dropdown
action = st.selectbox("Choose an action:", ["Select an Option", "Translate Text", "Generate Speech"])

# If "Translate Text" is selected
if action == "Translate Text":
    # Language selection for translation (exclude the input language)
    translation_lang = st.selectbox("Select the language to translate to:", 
                                    ["English", "Hindi", "Marathi", "French", "Spanish", "German"])

    if translation_lang:
        if st.button("Translate"):
            # Translate the text
            translator = Translator()
            translated = translator.translate(text_input, dest=translation_lang.lower())
            st.session_state.translated_text = translated.text
            st.session_state.translate_action = True
            st.session_state.selected_language = translation_lang

            st.success(f"Text translated to {translation_lang} successfully!")
            st.write("Translated Text:", st.session_state.translated_text)

        # Option to either show the translated text or generate speech from the translated text
        if st.session_state.translate_action:
            next_action = st.selectbox("What would you like to do next?",
                                       ["Select an Option", "Generate Speech from Translated Text", "Show Only Translated Text"])

            if next_action == "Show Only Translated Text":
                st.write("Here is your translated text:")
                st.write(st.session_state.translated_text)

            # Generate speech from translated text
            elif next_action == "Generate Speech from Translated Text":
                if st.button("Generate Speech from Translated Text"):
                    with st.spinner("Generating speech..."):
                        try:
                            # Use gTTS to convert text to speech (no voice selection)
                            tts = gTTS(text=st.session_state.translated_text, lang='en', slow=False)
                            audio_path = "generated_speech.mp3"
                            tts.save(audio_path)

                            # Provide the audio for playback in Streamlit
                            st.audio(audio_path)
                            st.success("Speech generated successfully from the translated text!")
                            st.download_button("Download Speech", audio_path)

                        except Exception as e:
                            st.error(f"Error generating speech: {e}")

# If "Generate Speech" is selected directly
elif action == "Generate Speech":
    if st.button("Generate Speech"):
        with st.spinner("Generating speech..."):
            try:
                # Use gTTS to convert text to speech (no voice selection)
                tts = gTTS(text=text_input, lang='en', slow=False)
                audio_path = "generated_speech.mp3"
                tts.save(audio_path)

                # Provide the audio for playback in Streamlit
                st.audio(audio_path)
                st.success("Speech generated successfully!")
                st.download_button("Download Speech", audio_path)

            except Exception as e:
                st.error(f"Error generating speech: {e}")

# Footer with dark mode toggle and preferences
st.markdown("""
    <div style='text-align: center; padding-top: 20px;'>
    <small>🌙 Click <strong>Preferences</strong> in the Streamlit menu for Dark Mode.</small>
    </div>
""", unsafe_allow_html=True)
