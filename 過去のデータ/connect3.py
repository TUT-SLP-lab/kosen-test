import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)

prompt = """
#命令
あなたは薬剤師です。
以下の条件をもとに次の
#条件

"""

import whisper
import json
model = whisper.load_model("small") #モデル指定
result = model.transcribe("Record.mp3", verbose=True, fp16=False, language="ja") #ファイル指定
print(result['text'])

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": result['text'],
        }
    ],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)


speech_file_path = "connect.wav"
response = client.audio.speech.create(
    model ="tts-1",
    voice ="fable",
    input = chat_completion.choices[0].message.content
)

response.stream_to_file(speech_file_path)
f = open('transcription.txt', 'w', encoding='UTF-8')
f.write(json.dumps(result['text'], sort_keys=True, indent=4, ensure_ascii=False))
f.close()