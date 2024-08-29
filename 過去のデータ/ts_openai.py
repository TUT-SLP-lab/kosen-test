import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key=API_KEY,
)


print("exit or quit で会話を終了")
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("会話終了")
        break

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="gpt-4o-mini",
    )

    print("AI:", chat_completion.choices[0].message.content)

