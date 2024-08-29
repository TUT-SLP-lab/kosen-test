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


def translation(qusetion):
    prompt1 = f"""
    質問:{qusetion}
    質問文を英語に翻訳して
    """
    prompt2 = call_langchain(prompt1, models[0])
    prompt3 = f"""
    質問:{prompt2}
    質問文を日本語に翻訳して
    """
    result = call_langchain(prompt3, models[0])
    return result


text = "x**3-6*x**2+11*x-6を因数分解して" 
answer = translation(text)
print(answer)
