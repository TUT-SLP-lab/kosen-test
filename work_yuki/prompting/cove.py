import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')


client = OpenAI(api_key=API_KEY)

prompt1 = """
Q: 質問1
A: 1の答え
Q: 質問2
A: 2の答え
Q: 質問3
A:
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt1,}],
    model="gpt-4o-mini",
)
output1 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

prompt2 = """
Context: Q:質問1
A:1の答え
Response:
1の答えに含まれている事実，それを検証するための質問
1の答えに含まれている事実，それを検証するための質問

Context: Q:質問2
A:2の答え
Response:
2の答えに含まれている事実，それを検証するための質問
2の答えに含まれている事実，それを検証するための質問

Context: Q:質問3
A:{output1_}
Response:
""".format(output1_=output1)

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt2,}],
    model="gpt-4o-mini",
)
output2 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)


prompt3_1 = """
Q:検証するための質問
A:答え

Q:検証するための質問
A:答え

Q:先ほど生成した質問
A:
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt3_1,}],
    model="gpt-4o-mini",
)
output3_1 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

prompt3_2 = """
Q:検証するための質問
A:答え

Q:検証するための質問
A:答え

Q:先ほど生成した質問
A:
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt3_2,}],
    model="gpt-4o-mini",
)
output3_2 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)

prompt4 = """
Context:修正前の文章
別のソースからの情報
検証ステップの実行結果:Q + A
検証ステップの実行結果:Q + A
Response:修正された一貫性のある文章

Context:修正前の文章
別のソースからの情報
検証ステップの実行結果:Q + A
検証ステップの実行結果:Q + A
Response:修正された一貫性のある文章

Context:prompt1の答え
別のソースからの情報
検証ステップの実行結果:Q(prompt2の質問) + A:{output3_1_}
検証ステップの実行結果:Q(prompt2の質問) + A:{output3_2_}
Response:
""".format(output3_1_= output3_1, output3_2_= output3_2)

chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt4,}],
    model="gpt-4o-mini",
)
output4 = chat_completion.choices[0].message.content
print(chat_completion.choices[0].message.content)