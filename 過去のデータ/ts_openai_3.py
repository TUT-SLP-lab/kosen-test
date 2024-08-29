import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)

user_text = "アイスについて1文で教えてください。"
prompt = """
質問1: 「世界で最も美しいビーチは何ですか？」と質問2:「最も美しいビーチは何ですか？」、
これら2つの質問がお互いの言い換えであるかどうかを判断してください。
"""
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

prompt1 = """
Role:あなたは非常に言語能力に秀でている人です。
質問1: 「世界で最も美しいビーチは何ですか？」と質問2:「最も美しいビーチは何ですか？」、
これら2つの質問がお互いの言い換えであるかどうかを判断してください。
Q:両方の質問に対するあなたの理解を明確にしてください。
A:
"""
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

prompt2 = """
質問1: 「世界で最も美しいビーチは何ですか？」と質問2:「最も美しいビーチは何ですか？」、
これら2つの質問がお互いの言い換えであるかどうかを判断してください。
Q:両方の質問に対するあなたの理解を明確にしてください。
A:{output1_}
Q:主題、文脈、意味内容に基づく類似性の予備的識別を行う。
A:
"""
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

prompt3 = """
質問1: 「世界で最も美しいビーチは何ですか？」と質問2:「最も美しいビーチは何ですか？」、
これら2つの質問がお互いの言い換えであるかどうかを判断してください。
Q:両方の質問に対するあなたの理解を明確にしてください。
A:{output1_}
Q:主題、文脈、意味内容に基づく類似性の予備的識別を行う。
A:{output2_}
Q:予備的な分析を批判的に評価する。質問がパラフレーズであるという最初の評価に確信が持てない場合は、再評価を試みる。
A:
"""
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