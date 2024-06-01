# StreamSpeak_GPT_Assistant


This Streamlit app serves as a virtual assistant powered by ChatGPT, allowing users to interact with it through speech input and receive responses generated by an AI model.

## Introduction

Hi there! I'm here to make your life easier – what can I assist you with?

## Features

- Voice recognition: Utilizes the `speech_recognition` library to recognize speech input from the user through the microphone.
- Text-to-speech conversion: Converts user input and AI-generated responses into audio using the `gTTS` library.
- ChatGPT integration: Interacts with the OpenAI ChatInterpreter for generating responses based on user queries.
- Interactive UI: Displays user input and AI responses in a visually appealing interface using Streamlit.
- Sidebar customization: Allows users to see the introduction and status updates in the sidebar.

## Usage

1. Run the Streamlit app.
2. Speak into the microphone to ask a question or provide a query.
3. Wait for the virtual assistant to process the input and generate a response.
4. Listen to the response through audio playback.
5. Continue the conversation as needed.

## Installation

To run this app locally, make sure you have the required libraries installed:

```bash
pip install streamlit speech_recognition pydub gtts azure-cognitiveservices-speech

``bash
streamlit run application.py
