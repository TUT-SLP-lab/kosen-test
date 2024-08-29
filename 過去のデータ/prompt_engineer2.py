import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)

"""
import os
os.environ["OPENAI_API_KEY"] = API_KEY

from langchain_openai import ChatOpenAI
llm = ChatOpenAI()
llm.invoke("高専とはなんですか")
"""

user_text = "西暦2000年に何がありましたか"
user_text_change = "「" + user_text +"」の問を言い換えてください。言い換えた文章だけを示してください"

print(user_text)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_text_change,
        }
    
    ],
    model="gpt-4o-mini",
)
print(chat_completion.choices[0].message.content)
user_text_change= chat_completion.choices[0].message.content

#user_text1 = chat_completion.choices[0].message.content
#user_text = "「" + user_text + "」に対する回答は「" + user_text1 +"」でした。" + "このことについてこの情報は正しいか判断してください"

print(user_text)
print(user_text_change)

user_text_question1 = "「" + user_text +"」と" + user_text_change + "の両方の質問に対するあなたの理解度を明確にしてください。さらに予備的な分析を批判的に評価してください。また、自分の分析に対する確信度を評価し、その確信度の説明をしてください。"
print(user_text_question1)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_text_question1,
        }
    
    ],
    model="gpt-4o",
)
print(chat_completion.choices[0].message.content)
user_text_question1= chat_completion.choices[0].message.content
