
def test(input_text:str) -> str:
    return "Hello, " + input_text 

if __name__ == "__main__":
    from openai import OpenAI
    from time import sleep
    import json
    from tqdm import tqdm
    from dotenv import load_dotenv
    
    load_dotenv()

    class BatchService:
        def __init__(self):
            self.inputs = []
            self.models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
            self.system_message = "あなたは役にたつアシスタントです。ユーザの問題に正確な答えを提供します。"
            self.client = OpenAI()


        def add_text(self, text:str):
            self.inputs.append({"text":text, "custom_id": f"request-{len(self.inputs)}"})

        def process(self):
            tq = tqdm(self.models)
            for model in tq:
                jsonl = ""
                for item in self.inputs:
                    jsonl += '{"custom_id": "' + item["custom_id"] + '", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "' + model + '", "messages": [{"role": "system", "content": "' + self.system_message + '"},{"role": "user", "content": "' + item["text"] + '"}],"max_tokens": 1000}}\n'

                with open("tmp/batch_input.jsonl", "w", encoding="utf-8") as f:
                    f.write(jsonl)

                tq.set_description(f"Sending request to {model}")

                with open("tmp/batch_input.jsonl", "rb") as f:
                    batch_input_file = self.client.files.create(file=f, purpose="batch")

                

                batch_input_file_id = batch_input_file.id

                batch_object = self.client.batches.create(
                    input_file_id=batch_input_file_id,
                    endpoint='/v1/chat/completions',
                    completion_window="24h",
                    metadata={"description": "Chat completions for multiple models"}
                )


                processing = ["validating", "in_progress", "finalizing", "cancelling"]
                while batch_object.status in processing:
                    tq.set_description(f"{model}: {batch_object.status.upper()}")
                    sleep(10)
                    batch_object = self.client.batches.retrieve(batch_object.id)

                tq.set_description(f"{model}: {batch_object.status.upper()}")

                if batch_object.errors is not None:
                    print(batch_object.errors)

                if not batch_object.output_file_id is None:
                    response = self.client.files.content(batch_object.output_file_id)
                    
                    for line in response.text.split("}\n{"):
                        line = line.strip()
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
                        custom_id = line["custom_id"]
                        result = {"model": model, "output":line["response"]["body"]["choices"][0]["message"]["content"]}

                        for item in self.inputs:
                            if item["custom_id"] == custom_id:
                                result["input"] = item["text"]
                                break
                        with open(f"out/{custom_id}-{model}.json", "w", encoding="utf-8") as f:
                            f.write(json.dumps(result, ensure_ascii=False, indent=2))

    batch = BatchService()
    
    with open("test/input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            in_txt = line.strip()
            batch.add_text(in_txt)
    batch.process()