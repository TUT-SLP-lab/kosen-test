from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)

speech_file_path = "./data/speech.wav"
response = client.audio.speech.create(
  model="tts-1",
  voice="fable", # alloy, echo, fable, onyx, nova, shimmer
  input="こんにちは。がちもとです。今日は、オープンエーアイでテキストから音声合成していきます！"
)

response.stream_to_file(speech_file_path)