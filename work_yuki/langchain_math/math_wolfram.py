from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
WOLFRAM_ALPHA_APPID = os.getenv('WOLFRAM_ID')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["WOLFRAM_ALPHA_APPID"] = WOLFRAM_ALPHA_APPID

question = """
x**3-6*x**2+11*x-6を因数分解して
"""

chat = ChatOpenAI(
    model_name="gpt-4o-mini",
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

print(f"\n{result.content}")
 
filename = 'langchain.txt'
f = open(filename, 'w')
f.write(f'{result.content}\n')
f.close()