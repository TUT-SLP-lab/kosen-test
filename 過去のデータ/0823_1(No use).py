import os
from dotenv import load_dotenv

#env内のAPIを取得
load_dotenv('.env')
API_KEY = os.getenv('OPENAI_KEY')

os.environ["OPENAI_API_KEY"] = API_KEY

import os
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator

from langchain.document_loaders import YoutubeLoader

youtube_url = "https://www.youtube.com/watch?v=rqnEglqS6DI"

loader = YoutubeLoader.from_youtube_url(youtube_url,language="ja")

index = VectorstoreIndexCreator(
    vectorstore_cls=Chroma,
    embedding=OpenAIEmbeddings(disallowed_special=()),).from_loaders([loader])
    
question = "要約して"
answer = index.query(question)
print(answer)


