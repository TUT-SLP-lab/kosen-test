import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client1 = OpenAI(api_key=API_KEY)
client2 = OpenAI(api_key=API_KEY)

text = "日本で起きた千年に起きたことをまとめて"
output1 = []
output2 = []

def call_chatgpt1(text):
    chat_completion1 = client1.chat.completions.create(
        messages=[{"role": "user",
                "content": text,}],
        model="gpt-4o-mini",
    )
    output1.append(chat_completion1.choices[0].message.content)
    print("chatgpt1")
    print(chat_completion1.choices[0].message.content)

def call_chatgpt2(text):
    chat_completion2 = client2.chat.completions.create(
        messages=[{"role": "user",
                "content": prompt1,}],
        model="gpt-4o-mini",
    )
    output2.append(chat_completion2.choices[0].message.content)
    print("chatgpt2")
    print(chat_completion2.choices[0].message.content)

call_chatgpt1(text)
prompt1 = f"""
質問: {text}
回答: {output1[0]}
上記の質問に対する回答は内容は正しいですか?
"""
print(prompt1)
print("-------")
call_chatgpt2(prompt1)