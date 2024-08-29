import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)

text = "あなたは薬剤師です。解熱鎮痛剤について教えて下さい"
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

prompt1 = f"""
Q: {text}
上記の質問に対する回答として考えられるものを出力してください．
"""
call_chatgpt(prompt1)
prompt2 = f"""
Q: {text}
A: {output[0]}
上記の回答が正しい前提はなんですか?
"""
call_chatgpt(prompt2)
prompt3 = f"""
Q: {text}
A: {output[0]}
前提: {output[1]}
上記の回答を仮説として考えると，前提に合致していますか?
"""
call_chatgpt(prompt3)