from test_gpt import test
import os

def main():
    with open("test/input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            in_txt = line.strip()
            out_txt = test(in_txt)

            with open(f"out/output_{i}.txt", "a", encoding="utf-8") as f:
                f.write(in_txt + "\n\n")
                f.write(out_txt + "\n")
        
main()