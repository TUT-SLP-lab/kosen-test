import os
from openai import OpenAI
import os
from dotenv import load_dotenv

def generate_text(model_name,system_message,user_message):
    load_dotenv('.env')
    API_KEY = os.getenv('OPENAI_KEY')
    client = OpenAI(
        api_key=API_KEY,
    )
    
    chat_completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role":"system","content": system_message},
            {"role":"user","content": user_message} #変更する場所:user_message -> result['text'] 
        ]
    )
    return chat_completion.choices[0].message.content


import whisper
import json

talk_counter = 0



if talk_counter == 0:
    model = whisper.load_model("small") #モデル指定
    result = model.transcribe("Record.mp3", verbose=True, fp16=False, language="ja") #ファイル指定
    print(result['text'])
    talk_counter = talk_counter + 1
else:
    while talk_counter > 10:
        model = whisper.load_model("small") #モデル指定
        result = model.transcribe("result['text']", verbose=True, fp16=False, language="ja") #ファイル指定            
        print(result['text'])
        talk_counter = talk_counter + 1

    model_name = "gpt-4"
    system_message ="あなたは薬剤師です。条件として、文字数は400文字程度、重要なキーワードを含める、小学生でもわかる簡潔な文章"
    #命令・条件の入力
    user_message = "こんにちは。風邪によく効く薬を教えてください"
    #指定メッセージ
    
    generate_text = generate_text(model_name, system_message, user_message)
    
    print(generate_text)

# response.stream_to_file(speech_file_path)
f = open('transcription.txt', 'w', encoding='UTF-8')
f.write(json.dumps(user_message, sort_keys=True, indent=4, ensure_ascii=False))
f.close()