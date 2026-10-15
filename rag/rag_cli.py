import json
import sys

from rag_answer import ask_rag


def main():
    input_data = json.loads(sys.stdin.read())

    input_text = input_data["input_text"]

    result = ask_rag(input_text)

    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()