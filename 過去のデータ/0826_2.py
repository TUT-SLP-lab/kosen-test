import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, load_tools
from langchain_openai import ChatOpenAI
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

# envの読み込み
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
os.environ["OPENAI_API_KEY"] = API_KEY

#API_KEYの入力
client = OpenAI(api_key=API_KEY)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Few-shot
examples = [
    {"input": "3+5の値は？", "output": "8である。"},
    {"input": "10×20の値は？", "output": "200である。"},
    {"input": "50÷2の値は？", "output": "25である。"}
]

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

vectorstore = Chroma(
    examples,
    embedding_model,
    collection_name="few-shot-examples"
)

example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore, k=3
)

few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_selector=example_selector,
    example_prompt_template=ChatPromptTemplate.from_messages([
        {"role": "user", "content": "{input}"},
        {"role": "assistant", "content": "{output}"}
    ]),
    chat_prompt_template=ChatPromptTemplate.from_messages([
        {"role": "user", "content": "{input}"}
    ])
)

set1 = """
### 出力形式:
・200~300字
・で・ある調を使用
・です・ます調は禁止
"""

# few-shot
def agents(setting, question):
    messages = few_shot_prompt_template.format_prompt(
        {"input": question}
    ).messages
    answer = llm(messages=messages)
    return answer

# 質問
text_question = "15989×245の値は"

text_answer = agents(set1, text_question)


# モデルを使った回答生成
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

# 正誤・どちらでもない
text_true = f"「{text_answer}」が「{text_question}」に対して正確であり、その理由と根拠を明確に"
text_false = f"「{text_answer}」が「{text_question}」に対して不正確であり、その理由と根拠を明確に"
text_uncertain = f"「{text_answer}」は「{text_question}」に対して正しいとも間違っているとも言えない場合、その理由と根拠を簡潔に"

text_true_answer = gpt("True回答", "gpt-4o", set1, text_true)
text_false_answer = gpt("False回答", "gpt-4o", set1, text_false)
text_uncertain_answer = gpt("Uncertain回答", "gpt-4o", set1, text_uncertain)

# 最終判断
text_final = f"「{text_question}」に関して、以下の判断：" + \
    f"「{text_answer}」、「{text_true_answer}」、「{text_false_answer}」、「{text_uncertain_answer}」" + \
    "これらの根拠を踏まえた上で、最終的にこの質問に対する答え:"

text_final_answer = gpt("最終的な回答", "gpt-4o-mini", set1, text_final)