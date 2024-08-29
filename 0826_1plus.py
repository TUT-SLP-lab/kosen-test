import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, load_tools
from langchain_openai import ChatOpenAI
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)

# envの読み込み
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
os.environ["OPENAI_API_KEY"] = API_KEY

#API_KEYの入力
client = OpenAI(api_key=API_KEY)

# few-shot prompting
#set1 = [
#    {"input"}
#]




llm = ChatOpenAI(model="gpt-4o", temperature=0)
tool_names = ["ddg-search"]
tools = load_tools(tool_names, llm=llm)

agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

# few-shot(gpt)
set1 ="""
### 出力形式:
・200~300字
・で・ある調を使用
・です・ます調は禁止
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
    print(select)
    print(chat_completion.choices[0].message.content)
    print("--------------------\n")
    return chat_completion.choices[0].message.content

# langchain_agent
def agents(setting,question):
    answer = agent.invoke(question)
    
    return answer

#質問
text_question = """豊橋市はブラックサンダーが有名である。マルかバツか
"""

# langchainを使用した回答
text_answer = agents(set1,text_question)
print(text_answer)
# モデルを使った回答生成
# text_answer = chat("通常の回答(3.5)", "gpt-3.5-turbo", set1, text_question)

# 正誤・どちらでもない(agents.Ver)
text_true = f"「{text_answer}」は正確である、その理由と根拠を明確に"
text_false = f"「{text_answer}」は不正確である、その理由と根拠を明確に"
text_uncertain = f"「{text_answer}」は正しいとも間違っているとも言えない、その理由と根拠を簡潔に"

# 正誤・どちらでもない(gpt.Ver)
# text_true = f"「{text_answer}」が「{text_question}」に対して正確である、その理由と根拠を明確に"
# text_false = f"「{text_answer}」が「{text_question}」に対して不正確である、その理由と根拠を明確に"
# text_uncertain = f"「{text_answer}」は「{text_question}」に対して正しいとも間違っているとも言えない、その理由と根拠を簡潔に"

text_true_answer = gpt("True回答", "gpt-4o-mini", set1, text_true)
text_false_answer = gpt("False回答", "gpt-4o-mini", set1, text_false)
text_uncertain_answer = gpt("Uncertain回答", "gpt-4o-mini", set1, text_uncertain)

#最終判断(agents.Ver)
text_final = f"「{text_answer}」に関して、以下の判断："+ \
    f"「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
    "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

#最終判断(gpt.Ver)
#text_final = f"「{text_question}」に関して、以下の判断："+ \
#    f"「{text_answer}」、「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
#    "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

text_final_answer = gpt("最終的な回答", "gpt-4o", set1, text_final)
