import os
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
WOLFRAM_ALPHA_APPID = os.getenv('WOLFRAM_ID')
GOOGLE_API_KEY = os.getenv('GOOGLE_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_ID')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["WOLFRAM_ALPHA_APPID"] = WOLFRAM_ALPHA_APPID
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]


def call_math_wolfram(question, model):
    chat = ChatOpenAI(
        model_name=model,
        temperature=0,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
    )
    llm = OpenAI(temperature=0)
    tools = load_tools(['wolfram-alpha'])
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)

    result_en = agent.run(f"{question}")
    text = f"""
    以下の分を日本語にして
    {result_en}
    """
    messages = [HumanMessage(content=text)]
    result = chat(messages)
    return result

def call_google_search(question, model):
    llm = ChatOpenAI(model_name=model)
    tools = load_tools(["google-search"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    result = agent.run(f"{question}")
    return result

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

def call_choice(question, model1, model2, model3):
    result1 = call_math_wolfram(question, model1)
    result2 = call_google_search(question, model2)
    prompt = f"""
    質問:{question}
    回答1:{result1}
    回答2:{result2}
    質問と回答1,回答2をもとに、回答をさくせいして
    ただし、回答1,回答2が間違えている可能性があるため注意しなさい
    出力には回答1および回答2が間違えている可能性があるため、慎重に検証しましたなど余分な文章は入れないこと
    """
    result3 = call_langchain(prompt, model3) 
    return result3

text = """
x**3-6*x**2+11*x-6を因数分解して
"""
output = call_choice(text, models[1], models[1], models[0])
print(output)