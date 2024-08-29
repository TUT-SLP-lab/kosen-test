import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=API_KEY)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "現在の総理大臣は",
        }
    ],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)