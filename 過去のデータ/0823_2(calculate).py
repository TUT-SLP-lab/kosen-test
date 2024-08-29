import os
from openai import OpenAI
import os
from dotenv import load_dotenv

#env内のAPIを取得
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType, initialize_agent, load_tools

llm = OpenAI(temperature = 0.9, openai_api_key=API_KEY)

tool_names = ["llm-math"]
tools = load_tools(tool_names, llm=llm)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.run("""1334*58""")




