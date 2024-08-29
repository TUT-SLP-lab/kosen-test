import os
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client_a = OpenAI(api_key=API_KEY)
client_b = OpenAI(api_key=API_KEY)
client_c = OpenAI(api_key=API_KEY)

def call_chatgpt(text,models,reply,client):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user","content": text}],
        model = models,
    )
    reply.append(chat_completion.choices[0].message.content)
    print("----------")

def save_output_to_file(output, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, item in enumerate(output):
            file.write(f"Response {i+1}: {item}\n\n")


models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
output = []
result = []
result_list = [0, 0, 0]

text = """
同一方向に進行しながら進路変更する場合の合図の時期は、その行為をする３０メートル手前に達したときである。
〇か×で答え、理由も答えよ
"""

call_chatgpt(text, models[1], output, client_a)
print(text)
print(output[0])

prompt_ture = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、正しいと仮定して肯定的な回答を作成してしてください
"""
prompt_false = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、正しくないと仮定して否定的な回答を作成して出力してください
"""
prompt_ture = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、誤りがある場合は修正して添削した回答を作成して出力してください
"""

call_chatgpt(prompt_ture, models[0], output, client_b)
print("肯定的な回答")
print(output[1])
call_chatgpt(prompt_false, models[0], output, client_b)
print("否定的な回答")
print(output[2])
call_chatgpt(prompt_ture, models[0], output, client_b)
print("添削した回答")
print(output[3])

prompt = f"""
質問: {text}
回答1: {output[1]}
回答2: {output[2]}
回答3: {output[3]}
質問に対する3つの回答のうち正しい回答を選び、回答の番号を1,2,3の数字を1つ出力しなさい
回答は1,2,3の数字を、1つを出力しなさい。また、数字以外の文字は出力してはいけない
「正しい回答は「3」です。」など文章で出力してはいけない
"""

for i in range(20):
    call_chatgpt(prompt, models[np.random.randint(0,5)], result, client_c)
    num = int(result[i])
    result_list[num - 1] += 1
print(result)
print(result_list)
ax_index = np.argmax(result_list)
result_word = f"""回答{ax_index+1}:{output[ax_index+1]}"""

print(result_word)

#ファイルに書き込み
save_output_to_file(output, 'chatgpt_responses.txt')
print("Responses have been saved to 'chatgpt_responses.txt'.")