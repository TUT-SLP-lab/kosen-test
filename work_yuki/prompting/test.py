import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)

text = "通信規格ついて検索してレポートを作成して"
output = []

def call_chatgpt(text):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user",
            #"content": text,
            "content": text}],
        model="gpt-4o-mini",
    )
    output.append(chat_completion.choices[0].message.content)
    print("----------")
    print(chat_completion.choices[0].message.content)

call_chatgpt(text)