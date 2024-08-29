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
def clients(message):
    chat_completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system","content": "あなたは病院で薬を貰いに来た患者です。薬剤師と会話しています。患者になりきって話してください。" },
            {"role": "user","content": message},
        ],
    )
    print("患者:")
    print(chat_completion.choices[0].message.content)
    answer = chat_completion.choices[0].message.content
    return answer

def expert(message):
    chat_completion = client.chat.completions.create(
        model = "gpt-4o",
        
        messages=[
            {"role": "system","content": "あなたはベテランの薬剤師です。患者と会話をしています。薬剤師になりきって話してください" },
            {"role": "user","content": message},
        ],
    )
    print("薬剤師:")
    print(chat_completion.choices[0].message.content)
    answer = chat_completion.choices[0].message.content
    return answer

#client_ans = [ ]
#expert_ans = [ ]

i = 0
while i < 10:
    if i == 0:
        client_ans = clients("最初の会話内容を考えて、患者の最初の会話のみを出力してください。鍵括弧は必要ありません。")
    else:
        client_ans = clients("「"+ expert_ans + "」の会話から次の会話の応答を考えて、患者の次の会話のみを出力してください。鍵括弧は必要ありません。")
    
    expert_ans = expert("「" + client_ans + "」の会話から次の会話の応答を考えて、薬剤師の次の会話のみを出力してください。鍵括弧は必要ありません。")
    i = i + 1


