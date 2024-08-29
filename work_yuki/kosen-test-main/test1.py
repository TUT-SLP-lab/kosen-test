import os
import numpy as np
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
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


def call_chatgpt(text,models,reply,client):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user","content": text}],
        model = models,
    )
    reply.append(chat_completion.choices[0].message.content)
    #print("----------")

def save_output_to_file(output, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, item in enumerate(output):
            file.write(f"Response {i+1}: {item}\n\n")


def call_ture_or_false(question, model):
    output = []
    result = []
    result_list = [0, 0, 0]
    client = OpenAI(api_key=OPENAI_API_KEY)
    call_chatgpt(question, model, output, client) 
    #print(text)
    #print(output[0])

    prompt_ture = f"""
    質問: {question}
    回答: {output[0]}
    質問と回答の内容より、正しいと仮定して肯定的な回答を作成してしてください
    """
    prompt_false = f"""
    質問: {question}
    回答: {output[0]}
    質問と回答の内容より、正しくないと仮定して否定的な回答を作成して出力してください
    """
    prompt_ture = f"""
    質問: {question}
    回答: {output[0]}
    質問と回答の内容より、誤りがある場合は修正して添削した回答を作成して出力してください
    """
    call_chatgpt(prompt_ture, model, output, client)
    call_chatgpt(prompt_false, model, output, client)
    call_chatgpt(prompt_ture, model, output, client)
    #print("肯定的な回答")
    #print(output[1])
    #print("否定的な回答")
    #print(output[2])
    #print("添削した回答")
    #print(output[3])

    prompt = f"""
    質問: {question}
    回答1: {output[1]}
    回答2: {output[2]}
    回答3: {output[3]}
    質問に対する3つの回答のうち正しい回答を選び、回答の番号を1,2,3の数字を1つ出力しなさい
    回答は1,2,3の数字を、1つを出力しなさい。また、数字以外の文字は出力してはいけない
    「正しい回答は「3」です。」など文章で出力してはいけない
    """

    for i in range(10):
        call_chatgpt(prompt, models[np.random.randint(0,5)], result, client)
        num = int(result[i])
        result_list[num - 1] += 1
    #print(result)
    #print(result_list)
    ax_index = np.argmax(result_list)
    #result_word = f"""回答{ax_index+1}:{output[ax_index+1]}"""
    result_word = f"""回答:{output[ax_index+1]}"""
    return result_word


def translation(qusetion):
    prompt1 = f"""
    質問:{qusetion}
    日本語の質問を英語に翻訳して
    """
    prompt2 = call_langchain(prompt1, models[0])
    prompt3 = f"""
    回答:{prompt2}
    英語の回答を日本語に翻訳して
    """
    result = call_langchain(prompt3, models[0])
    return result


def call_google_search(question, model):
    llm = ChatOpenAI(model_name=model)
    tools = load_tools(["google-search"], llm=llm)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    result = agent.run(f"{question}")
    return result


def call_class(question, model):
    prompt = f"""
    質問:{question}
    質問について、以下の項目に分類し数字を出力しなさい
    回答は1,2,3の数字を、1つを出力しなさい。また、数字以外の文字は出力してはいけない
    1.数学の問題,
    2.ture or falseの問題,
    3.時事問題,
    4.その他の問題,
    """
    result = call_langchain(prompt, model)      
    if 1 == int(result[0]):
        print("数学の問題だよ")
        result = call_math_wolfram(question,model[0])
    
    elif 2 == int(result[0]):
        print("ture or falseの問題だよ")
        result = call_ture_or_false(question, models[0])

    elif 3 == int(result[0]):
        print("時事問題だよ")
        result = call_langchain(question, models[0])

    elif 4 == int(result[0]):
        print("その他の問題だよ")
        result = translation(question)
    return result


def call_choice(question, model1, model2, model3):
    answer1 = call_class(question, model1)
    answer2 = call_google_search(question, model2)
    prompt = f"""
    質問:{question}
    回答1:{answer1}
    回答2:{answer2}
    質問と回答1,回答2をもとに、回答をさくせいして
    ただし、回答1,回答2が間違えている可能性があるため注意しなさい
    「出力には回答1および回答2が間違えている可能性があるため、慎重に検証しました」など余分な文章は入れないこと
    """
    result3 = call_google_search(prompt, model3) 
    return result3

def test(input_text:str) -> str:
    answer = call_choice(input_text, models[0], models[0], models[0])
    return answer

#質問を書く
#text = f"""
#2024年の台風10号について教えて
#""" 

#answer = test(text)
#print("------------")
#print(answer)


#f = open('answerfile.txt', 'w')
#f.write(answer)
#f.close()