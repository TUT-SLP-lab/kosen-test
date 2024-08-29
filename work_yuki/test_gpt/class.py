import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

def call_langchain(question, model):
    llm = ChatOpenAI(model_name=model)
    tool_names = ["llm-math"]
    tools = load_tools(tool_names, llm=llm)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )
    result = agent.run(question)
    return result


def call_class(question, model):
    prompt = f"""
    質問:{question}
    質問について、以下の項目に分類し数字を出力しなさい
    回答は1,2,3,4の数字を、1つを出力しなさい。また、数字以外の文字は出力してはいけない
    1.数学の問題,
    2.ture or falseの問題,
    3.時事問題,
    4.その他の問題,
    """
    result = call_langchain(prompt, model)      
    if 1 == int(result[0]):
        print("数学の問題だよ")
    elif 2 == int(result[0]):
        print("ture or falseの問題だよ")
    elif 3 == int(result[0]):
        print("時事問題だよ")
    elif 4 == int(result[0]):
        print("その他の問題だよ")


#質問を書く
text = f"""
現在のフランス大統領について教えて
""" 
call_class(text, models[0])