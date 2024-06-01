import json,os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import numpy as np
import json
from scipy.io.wavfile import write, read
import asyncio
import requests
import json
import datetime
import azure.cognitiveservices.speech as speechsdk
import hashlib
import base64



with open("config.json") as fp:
    config = json.load(fp)



with open("/Users/sushilkumarbarai/audio_streaming/.creds/azure_asr.json") as fp:
    credit = json.load(fp)


with open("/Users/sushilkumarbarai/audio_streaming/.creds/sushtts.json") as fp:
    oztts = json.load(fp)

subscription_key=credit['subscription_key']
service_region=credit['service_region']
tts_key=oztts['azure']

print(subscription_key)
print(service_region)
    

voicebot_params = config["voicebot_params"]
openapiurl=voicebot_params['intent_api']['openapi_url']
bear_token=voicebot_params['intent_api']['bear_token']
tts_url=voicebot_params['intent_api']['tts_url']
print(tts_url)




class OpenAIChatInterpreter:
    def __init__(self):
        self.subscription_key=credit['subscription_key']
        self.service_region=credit['service_region']

    def recognize(self, audio_file_path=None):
        try:
            # Read the audio file
            sample_rate, audio_data = read(audio_file_path)
            print(f"sample_rate ::: {sample_rate}")
            print(f"audio_data ::: {audio_data}")

            # Construct the request URL
            url = f"https://{self.service_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=detailed"

            # Headers for the authentication and content type
            headers = {
                'Ocp-Apim-Subscription-Key': self.subscription_key,
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=8000',
                'Accept': 'application/json',
                "language": "en-IN"
            }

            # Read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Send the request to the Azure Speech-to-Text API
            response = requests.post(url, headers=headers, data=audio_data)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            response_data = response.json()
            print(f"response_data ::: {response_data['DisplayText']}")
            recog_text=response_data["DisplayText"]

            return recog_text
        
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")



    def text_to_text_request(self, user_message=None):
        url=openapiurl
        api_key=bear_token
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        payload = {
            "model":  "gpt-3.5-turbo",
            "version": "2023-05-15",
            "temperature": 1,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        }
        response_data = requests.post(url, json=payload, headers=headers)
        response=response_data.json()
        if "response" in response and "choices" in response["response"]:
            for choice in response["response"]["choices"]:
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
        return "no data found"


    
    def text_to_speech(self,chat_gpt_response=None):
        print(f"chat_gpt_response ::: {chat_gpt_response}")
        intxt_utf8 = chat_gpt_response.encode('utf-8')
        chk = hashlib.md5(intxt_utf8).hexdigest()
        intxt_base64 = base64.b64encode(intxt_utf8).decode('utf-8')
        audio_file = "./chat_gpt_audio.wav"
        payload = {
            "text": intxt_base64,
            "sid": chk,
            "checksum": chk,
            "text_type": "text",
            "user": "ozonetel",
            "gender": "female",
            "audio_encoding": "wav",
            "sample_rate_hertz": 16000,
            "synthesizer_type": "standard",
            "speaking_rate": 1.0,
            "volume_gain_db": 0.0,
            "app_type": "tts",
            "grammar": "mtts",
            "api_key": tts_key,
            "language": "en-IN"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(tts_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        audio_bytes = base64.b64decode(response.json()["synthesized_audio"])
      #  print(f"audio_bytes ::: {audio_bytes}")
        with open(audio_file, "wb") as fp:
            fp.write(audio_bytes)
        return audio_file,chat_gpt_response


    def process(self,audio_file_path=None):
        audio_file_path=audio_file_path
        recog_text=self.recognize(audio_file_path=audio_file_path)
        response = self.text_to_text_request(user_message=recog_text)
        tts,chat_gpt_response=self.text_to_speech(chat_gpt_response=response)
        print(f"TTS ::: {tts}")
        return tts,chat_gpt_response
    






