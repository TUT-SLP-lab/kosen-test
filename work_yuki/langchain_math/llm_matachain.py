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


llm = ChatOpenAI(model_name="gpt-4o-mini")
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

result1 = agent.run("""5の3乗は？""")
result2 = agent.run(""""その答えに対して、πを掛け算するといくつになる？""")

print(f"\n{result1}")
print(f"\n{result2}")
