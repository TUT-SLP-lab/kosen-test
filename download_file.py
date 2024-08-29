from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

import openai
import json

client = openai.Client()

def download_file(file_id: str, file_name: str) -> None:
    file_response = client.files.content(file_id)
    for line in file_response.text.split("}\n{"):
        if not line.startswith("{"):
            line = "{" + line
        if not line.endswith("}"):
            line += "}"
        try:
            line = json.loads(line)
        except json.decoder.JSONDecodeError:
            try:
                print(line.encode().decode("unicode-escape"))
            except:
                print(line)
            continue
        print(line["response"]["body"]["choices"][0]["message"]["content"])
        print(line["response"]["body"]["choices"][0]["message"]["content"].encode().decode("unicode-escape"))