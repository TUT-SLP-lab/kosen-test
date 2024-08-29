#import json
#s1 = open('set.json','r')
#s2 = json.load(s1)

import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)

user_text = "2000年の出来事について一言で述べてください"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_text,
        }
    
    ],
    model="gpt-4o",
)

print(chat_completion.choices[0].message.content)

user_text1 = chat_completion.choices[0].message.content
user_text = "「" + user_text + "」に対する回答は「" + user_text1 +"」でした。" + "このことについてこの情報は正しいか判断してください"
print(user_text)

count = 0
while count < 5:
    count +=1
    print(count)
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": user_text,
        }
    
        ],
        model="gpt-4o-mini",
    )
    print(chat_completion.choices[0].message.content)