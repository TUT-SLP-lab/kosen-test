import os
from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)

result = []
result_list = [0, 0, 0, 0, 0]
qest_num = 5

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

text = """
交差点やその付近以外の場所で緊急自動車が近づいてきたときは、道路の左に寄って一時停止しなければならない。
正負を判定しなさい
"""
print(text)

for i in range(qest_num):
    call_chatgpt(text, models[np.random.randint(0,5)], output, client)
    print(output[i])


prompt = f"""
質問: {text}
回答1: {output[0]}
回答2: {output[1]}
回答3: {output[2]}
回答4: {output[3]}
回答5: {output[4]}
質問に対する{qest_num}つの回答のうち正しい回答を選び、回答の番号をint形式で1,2,3,4,5の数字で出力しなさい
1,2,3,4,5の数字を、1つを出力しなさい
"""

for i in range(20):
    call_chatgpt(prompt, models[np.random.randint(0,5)], result, client)
    num = int(result[i])
    print(num)
    result_list[num - 1] += 1
print(result)
print(result_list)
ax_index = np.argmax(result_list)
result_word = f"""回答{ax_index+1}:{output[ax_index+1]}"""

print(result_word)