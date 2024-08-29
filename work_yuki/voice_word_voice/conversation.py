import whisper
import json
import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=API_KEY)


model = whisper.load_model("small") #モデル指定
result = model.transcribe("./data/you.wav", verbose=True, fp16=False, language="ja") #ファイル指定
print(result['text'])


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": result["text"],
        }
    ],
    model="gpt-3.5-turbo",
)
print(chat_completion.choices[0].message.content)


speech_file_path = "./data/respawn_file.wav"
response = client.audio.speech.create(
  model="tts-1",
  voice="fable", # alloy, echo, fable, onyx, nova, shimmer
  input=chat_completion.choices[0].message.content
)
response.stream_to_file(speech_file_path)