import os
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=API_KEY)
text = "Q:イブプロフェンについて教えて"
prompt = """
主な用途、用法、副作用、飲み合わせ、注意点について教えて
また、参考文献についても示せして
""".format(text_ = text)


chat_completion = client.chat.completions.create(
    messages=[{"role": "user",
            #"content": text,
            "content": prompt,}],
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)