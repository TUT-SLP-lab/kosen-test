import numpy as np
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import ChatOpenAI
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.exceptions import OutputParserException

# envの読み込み
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
os.environ["OPENAI_API_KEY"] = API_KEY

# API_KEYの入力
client = OpenAI(api_key=API_KEY)

# few-shot prompting
#set1 = [
#    {"input"}
#]


llm = ChatOpenAI(model="gpt-4o", temperature=0.8)
tool_names = ["ddg-search"]
tools = load_tools(tool_names, llm=llm)

agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

# Take a Step Back (段階的推論)
set1 ="""
### あなたは難しい問いに対して推論します。
ユーザの質問に対しては、それを解決するための段階的な推論をする。
まず3つの仮説を列挙してから、最終回答を目指してください。
わからないものに関してはわからないと述べてください。

仮説1:<仮説の説明を200字以内で>
仮説2:<仮説の説明を200字以内で>
仮説3:<仮説の説明を200字以内で>
最終回答:<仮説に基づいた結論>

### 出力形式:
・で・ある調を使用
・です・ます調は禁止

### 条件:
・現在は2024年8月
"""
set_tmp = """
### あなたは半角数字1か2しか出力してはいけません。
"""
set_set ="""
### 条件
・現在などのニュアンスがある文章では「2024年」として扱う
・入力に指定がなければ、日本の内容として扱う
・英語に翻訳して出力
"""
set_set2 ="""
### あなたは英語を日本語に翻訳してください。
日本語の場合はそのまま出力してください。
"""

# gpt(モデルは別指定)
def gpt(select, model_name, setting, content):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": setting},
            {"role": "user", "content": content},
        ],
        model=model_name,
    )
    #print(select)
    #print(chat_completion.choices[0].message.content)
    #print("--------------------\n")
    return chat_completion.choices[0].message.content

# langchain_agent
def agents(setting,question):
    try:
        answer = agent.invoke(question)
    except OutputParserException as e:
        print("エラーが発生。gpt処理へ移行")
        another = gpt("エラー処理","gpt-4o-mini",set1,str(e))
    return answer

#質問
question = """
昔のゲーム機について教えて
"""

text_tmp_jud = f"「{question}」についてこれが計算問題であれば1、計算問題でなければ2を出力"
text_tmp_answer = gpt("計算問題判断","gpt-4o-mini",set_tmp,text_tmp_jud)
print(text_tmp_answer)

#変数の定義(ifで定義されるため)
#text_answer = "null"

if text_tmp_answer == "1":
    print("計算問題:")

    tool_names = ["llm-math"]
    tools = load_tools(tool_names, llm=llm)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    text_answer = agent.run(question)
    print(text_answer)
    sys.exit("計算終了")

elif text_tmp_answer == "2":
    text_tmp_question = f"「{question}」について、条件に従って質問文だけ出力」"
    text_question = gpt("質問変更","gpt-4o-mini",set_set,text_tmp_question)
    print(text_question)
    # langchainを使用した回答
    text_answer = agents(set1,text_question)

    # モデルを使った回答生成
    # text_answer = chat("通常の回答(3.5)", "gpt-3.5-turbo", set1, text_question)

else:
    text_answer = "計算問題かどうかの判断ができませんでした。プログラムを終了します"
    print(text_answer)

# 正誤・どちらでもない(agents.Ver)
text_true = f"「{text_answer}」は正確である、その理由と根拠を明確に"
text_false = f"「{text_answer}」は不正確である、その理由と根拠を明確に"
text_uncertain = f"「{text_answer}」は正しいとも間違っているとも言えない、その理由と根拠を簡潔に"

# 正誤・どちらでもない(gpt.Ver)
# text_true = f"「{text_answer}」が「{text_question}」に対して正確である、その理由と根拠を明確に"
# text_false = f"「{text_answer}」が「{text_question}」に対して不正確である、その理由と根拠を明確に"
# text_uncertain = f"「{text_answer}」は「{text_question}」に対して正しいとも間違っているとも言えない、その理由と根拠を簡潔に"

text_true_answer = gpt("True回答", "gpt-4o-mini", set1, text_true)
text_false_answer = gpt("False回答", "gpt-3.5-turbo", set1, text_false)
text_uncertain_answer = gpt("Uncertain回答", "gpt-4o", set1, text_uncertain)

#最終判断(agents.Ver)
text_final = f"「{text_answer}」に関して、以下の判断："+ \
    f"「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
    "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

#最終判断(gpt.Ver)
#text_final = f"「{text_question}」に関して、以下の判断："+ \
#    f"「{text_answer}」、「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
#    "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

text_final_answer = gpt("最終的な回答", "gpt-4o", set1, text_final)

print("------------------------------------")

# text_answerからoutput部分のみを取り出す
output_only = text_answer.get('output', 'データが格納されていません')
output_tmp = f"「{output_only}」について日本語に翻訳してください。日本語の場合はそのまま出力して"
output = gpt("翻訳","gpt-4o", set_set2, output_tmp)
print(output)
print("")
print(text_final_answer)