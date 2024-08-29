import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)

text = "あなたは薬剤師です。解熱鎮痛剤について教えて下さい"

prompt1 = f"""
Q: {text}
上記の質問に対する回答として考えられるものを出力してください．
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt1,}],
    model="gpt-4o-mini",
)
output1 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

# 以下は各回答ごとに実行
prompt2 = f"""
Q: {text}
A: {output1}
上記の回答が正しい前提はなんですか?
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt2,}],
    model="gpt-4o-mini",
)
output2 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

prompt3 = f"""
Q: {text}
A: {output1}
前提: ${output2}
上記の回答を仮説として考えると，前提に合致していますか?
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt3,}],
    model="gpt-4o-mini",
)
output3 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

print(prompt1)
print(prompt2)
print(prompt3)