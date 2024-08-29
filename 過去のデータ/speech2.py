import os
from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY
    )

speech_file_path = "speech.wav"
response = client.audio.speech.create(
    model ="tts-1",
    voice ="fable",
    input = "こんにちは。音声合成のテストです。"
)

response.stream_to_file(speech_file_path)