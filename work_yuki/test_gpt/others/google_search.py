import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_ID')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

def call_google_search(question, model):
    llm = ChatOpenAI(model_name=model)
    tools = load_tools(["google-search"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    result = agent.run(f"{question}")
    return result

#ネット検索
text = f"""
例,2024年の台風について教えて
"""

result = call_google_search(text, models[1])
print("-------")
print(result)