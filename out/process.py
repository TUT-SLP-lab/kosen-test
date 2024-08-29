from glob import glob
import json

s = ""
files = [f for f in glob('request-*-gpt-4o.json')]
files.sort(key=lambda x: int(x.split('-')[1]))

for i, file in enumerate(files):
    with open(file) as f:
        data = json.load(f)
    
    s += f"***** input  {(i+1):02d} *****\n{data['input']}\n***** output {(i+1):02d} *****\n{data['output']}\n\n"

with open('output-gpt-4o.txt', 'w') as f:
    f.write(s)