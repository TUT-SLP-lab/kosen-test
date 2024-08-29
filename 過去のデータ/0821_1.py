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
def chat(select,model_name,content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
    
        ],
        model = model_name,
    )
    print("-----" + select + "-----")
    print(chat_completion.choices[0].message.content)
    print("--------------------\n")
    answer = chat_completion.choices[0].message.content
    return answer

def chat1(model_name,content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
    
        ],
        model = model_name,
    )
    answer = chat_completion.choices[0].message.content
    return answer

#質問部
text_question = input("質問を入力：")
text_answer = chat("通常の回答","gpt-3.5-turbo",text_question)

#Rephrase and Respond(RaR)
prompt1 = "「" + text_question + "」の質問を言い換えて、拡張し、そして答えてください"
text_prompt1 = chat("RaR言い換え1","gpt-3.5-turbo",prompt1)
prompt2 = "「" + text_prompt1 + "」は言い換えた質問とそれに対した答えです。それを使って元の質問に答えてください"
text_prompt2 = chat("RaR言い換え2","gpt-3.5-turbo",prompt2)


#True & False & Uncertain 判断
text_true = "「" + text_prompt1 + "」は「" + text_question + "」の対応関係は正しいです"
text_false = "「" + text_prompt1 + "」は「" + text_question + "」の対応関係は正しくありません"
text_uncertain = "「" + text_prompt1 + "」は「" + text_question + "」の対応関係はわかりません。どちらともいえない根拠を簡潔に述べてください。"

text_true_answer = chat("True回答","gpt-4o",text_true)
text_false_answer = chat("False回答","gpt-4o",text_false)
text_uncertain_answer = chat("Uncertain回答","gpt-4o",text_uncertain)

#総合判断部
#以上の質問回答を見て判断
text_final = "「" + text_question + "」の質問について" + "「" + text_prompt1 + "」「" + text_prompt2 + "」「" + text_answer + "」「" + text_true_answer + "」「" + text_false_answer + "」「"+ text_uncertain_answer + "」がありました。これらの情報から、質問に対する答えはどのようになるか述べてください。"
text_final_answer = chat("最終的な回答","gpt-4o-mini",text_final)

