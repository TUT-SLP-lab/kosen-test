import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client_a = OpenAI(api_key=API_KEY)
client_b = OpenAI(api_key=API_KEY)
client_c = OpenAI(api_key=API_KEY)

models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
output = []

def call_chatgpt(text,models,reply,client):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model = models,
    )
    reply.append(chat_completion.choices[0].message.content)
    print("----------")

def save_output_to_file(output, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, item in enumerate(output):
            file.write(f"""------------------------
    Response {i+1}: {item}\n\n""")


text = "柿田川湧水について教えて"
call_chatgpt(text, models[1], output, client_a)
print(text)
print(output[0])

prompt_ture = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、正しいと仮定して肯定的な回答を作成して
また、誤りがある場合は修正して回答を作成して
"""
prompt_false = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、正しくないと仮定して否定的な回答を作成して
"""
prompt_ture = f"""
質問: {text}
回答: {output[0]}
質問と回答の内容より、誤りがある場合は修正して添削した回答を作成して
"""

call_chatgpt(prompt_ture, models[1], output, client_b)
print("肯定的な回答")
print(output[1])
call_chatgpt(prompt_false, models[1], output, client_b)
print("否定的な回答")
print(output[2])
call_chatgpt(prompt_ture, models[1], output, client_b)
print("添削した回答")
print(output[3])

prompt = f"""
回答1: {output[1]}
回答2: {output[2]}
回答3: {output[3]}
この3つの回答のうち正しい回答を選んで、選んだ回答と回答内容を示して。
また、選んだ回答に正しくない個所がある場合、その個所を示して
"""

call_chatgpt(prompt, models[1], output, client_c)
print(output[4])

#ファイルに書き込み
save_output_to_file(output, 'chatgpt_responses.txt')
print("Responses have been saved to 'chatgpt_responses.txt'.")