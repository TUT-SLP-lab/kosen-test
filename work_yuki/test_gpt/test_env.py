import os 
from dotenv import load_dotenv

load_dotenv('.env')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
WOLFRAM_ALPHA_APPID = os.getenv('WOLFRAM_ID')
GOOGLE_API_KEY = os.getenv('GOOGLE_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_ID')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["WOLFRAM_ALPHA_APPID"] = WOLFRAM_ALPHA_APPID
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID

print(OPENAI_API_KEY)
print(WOLFRAM_ALPHA_APPID)
print(GOOGLE_API_KEY)
print(GOOGLE_CSE_ID)