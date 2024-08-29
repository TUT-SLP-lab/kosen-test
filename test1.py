import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException

# 環境変数の読み込み
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
os.environ["OPENAI_API_KEY"] = API_KEY

# OpenAIクライアントの初期化
client = OpenAI(api_key=API_KEY)

# Take a Step Back (段階的推論)
set1 = """
### あなたは難しい問いに対して推論します。
ユーザの質問に対しては、それを解決するための段階的な推論をする。
まず3つの仮説を列挙してから、最終回答を目指してください。
回答に関して曖昧さがある場合はわからないと述べてください。

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
set_set = """
### 条件
・現在などのニュアンスがある文章では「2024年」として扱う
・入力に指定がなければ、日本の内容として扱う
・英語に翻訳して出力
"""
set_set2 = """
### あなたは英語を日本語に翻訳してください。
日本語の場合はそのまま出力してください。
"""

# 質問に対する処理
def test(question: str) -> str:
    # gpt(モデルは別指定)
    def gpt(select, model_name, setting, content):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": setting},
                {"role": "user", "content": content},
            ],
            model=model_name,
        )
        return chat_completion.choices[0].message.content

    # エージェントの初期化とエラーハンドリング
    def agents(setting, question):
        try:
            answer = agent.invoke(question)
            es = 0
        except OutputParserException as e:
            print("エラーが発生。gpt処理へ移行")
            es = 1
            answer = gpt("エラー処理", "gpt-4o-mini", set1, question)
        except Exception as e1:
            raise e1
        return answer,es

    # ChatOpenAIの初期化
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tool_names = ["ddg-search"]
    tools = load_tools(tool_names, llm=llm)

    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )

    # 質問が計算問題かどうかの判定
    text_tmp_jud = f"「{question}」についてこれが計算問題であれば1、計算問題でなければ2を出力"
    text_tmp_answer = gpt("計算問題判断", "gpt-4o-mini", set_tmp, text_tmp_jud)
    print(text_tmp_answer)

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
        return text_answer

    elif text_tmp_answer == "2":
        text_tmp_question = f"「{question}」について、条件に従って質問文だけ出力」"
        text_question = gpt("質問変更", "gpt-4o-mini", set_set, text_tmp_question)
        print(text_question)
        text_answer,es = agents(set1, text_question)
    else:
        text_answer = "計算問題かどうかの判断ができませんでした。プログラムを終了します"
        print(text_answer)

    # 正確性の判定
    text_true = f"「{text_answer}」は正確である、その理由と根拠を明確に"
    text_false = f"「{text_answer}」は不正確である、その理由と根拠を明確に"
    text_uncertain = f"「{text_answer}」は正しいとも間違っているとも言えない、その理由と根拠を簡潔に"

    text_true_answer = gpt("True回答", "gpt-4o-mini", set1, text_true)
    text_false_answer = gpt("False回答", "gpt-3.5-turbo", set1, text_false)
    text_uncertain_answer = gpt("Uncertain回答", "gpt-4o", set1, text_uncertain)

    # 最終判断
    text_final = f"「{text_answer}」に関して、以下の判断：" + \
        f"「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
        "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

    text_final_answer = gpt("最終的な回答", "gpt-4o", set1, text_final)

    # 出力部分の処理
    if es == 0:
        output_only = text_answer.get('output', 'データが格納されていません')
    elif es == 1:
        output_only = text_answer
    
    output_tmp = f"「{output_only}」について日本語に翻訳してください。日本語の場合はそのまま出力して"
    output = gpt("翻訳", "gpt-4o", set_set2, output_tmp)
    out = output + "\n" + text_final_answer
    return out