import os
from openai import OpenAI
import os
from dotenv import load_dotenv

#env内のAPIを取得
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

os.environ["OPENAI_API_KEY"] = API_KEY

#client = OpenAI(
#    api_key=API_KEY,
#)

from langchain.agents import initialize_agent, load_tools
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

tool_names = ["ddg-search"]
tools = load_tools(tool_names, llm=llm)

agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

#agent.invoke("2024パリオリンピックで日本が取得した金メダルの数は")
agent.invoke(input("入力:"))