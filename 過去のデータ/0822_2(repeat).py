import os
from openai import OpenAI
import os
from dotenv import load_dotenv

#env内のAPIを取得
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)

# 主GPT部
def chat(model_name,setting,content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": setting,
                "role": "user",
                "content": content,
            }
    
        ],
        model = model_name,
    )
    print(chat_completion.choices[0].message.content)
    answer = chat_completion.choices[0].message.content
    return answer

#質問部
text_question = """経営戦略に基づいて策定される情報システム戦略の責任者はどの職位の人になりますか。
"""
ans = [0] * 10
i = 0
while i < 5:
    ans[i] = chat("gpt-4o"," ",text_question)
    i = i + 1
