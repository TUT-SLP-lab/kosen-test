from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
WOLFRAM_ALPHA_APPID = os.getenv('WOLFRAM_ID')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["WOLFRAM_ALPHA_APPID"] = WOLFRAM_ALPHA_APPID
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

text = """
x**3-6*x**2+11*x-6を因数分解して
"""
result = call_math_wolfram(text, models[0])
print(f"\n{result.content}")
