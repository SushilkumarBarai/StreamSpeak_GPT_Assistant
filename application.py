import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play
import os
from OpenAIChatInterpreter import OpenAIChatInterpreter
import streamlit.components.v1 as components

api = OpenAIChatInterpreter()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("I am listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        col1, col2 = st.columns([1, 8])
        with col1:
            st.image("user.png", width=50)  # Replace with your image path
        with col2:
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; color: black;'>{text}</div>", unsafe_allow_html=True)
        return text
    except sr.UnknownValueError:
        st.write("Could not understand audio. Please ask your query.")
        return None
    except sr.RequestError as e:
        st.write("Error:", e)
        return None

def convert_and_playback(text):
    tts = gTTS(text, lang='en')
    audio_file = "output.wav"
    tts.save(audio_file)
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(8000)
    audio.export("output_8k.wav", format="wav")
    recog_text, chat_gpt_response = api.process(audio_file_path="output_8k.wav")
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("bot.png", width=50)  # Replace with your image path
    with col2:
        st.markdown(f"<div style='background-color: #e8f5e9; padding: 10px; border-radius: 10px; color: black;'>{chat_gpt_response}</div>", unsafe_allow_html=True)
    return chat_gpt_response

def listen_and_continue():
    while True:
        text = recognize_speech()
        if text:
            audio_text = convert_and_playback(text)
            if audio_text:
                # Create an empty slot to display audio player
                audio_placeholder = st.empty()
                # Convert response text to speech and play the audio
                tts = gTTS(audio_text, lang='en')
                tts.save("response.wav")
                audio = AudioSegment.from_file("response.wav")
                play(audio)
                # Clear the empty slot after audio playback
                audio_placeholder.empty()
        else:
            pass

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center; font-size: 36px; color: #4CAF50;'><b><i>Virtual Assistance Powered by ChatGPT</i></b></h1>", unsafe_allow_html=True)
    
    # Adding a sidebar for additional options
    st.sidebar.title("Introduction")
    st.sidebar.markdown("Hi there! I'm here to make your life easier – what can I assist you with?")

    
    # Placeholder for status updates
    status_placeholder = st.sidebar.empty()
    
    # Adding an image in the sidebar
    st.sidebar.image("/Users/sushilkumarbarai/workspace/audio_streaming/utils/assitant.png", use_column_width=True)  # Replace with your image path
    
    # Injecting JavaScript for auto-scrolling
    auto_scroll_js = """
    <script>
    function scrollToBottom() {
        var mainDiv = parent.document.getElementsByClassName("main")[0];
        mainDiv.scrollTop = mainDiv.scrollHeight;
    }
    setInterval(scrollToBottom, 1000);
    </script>
    """
    
    # Displaying JavaScript in the app
    components.html(auto_scroll_js)
    
    listen_and_continue()
