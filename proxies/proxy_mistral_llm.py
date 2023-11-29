import os
import requests
import json
from transformers import AutoTokenizer
from utils.utils import ROOT_PATH

from llm.contexts.mistral_context import MistralContext


class ProxyMistralLLM:
    def __init__(self, endpoint_url: str):
        self.__endpoint_url = endpoint_url
        self.__tokenizer = AutoTokenizer.from_pretrained('TheBloke/Mistral-7B-Instruct-v0.1-GPTQ', use_fast=True, cache_dir=os.path.join(ROOT_PATH, "storage", "llms"))

    def ask(self, context: MistralContext) -> str:
        model_input_str = self.__tokenizer.apply_chat_template(context.messages, tokenize=False)
        # Prepare the data as a dictionary and convert it to a JSON string
        data = json.dumps({"query": model_input_str}, ensure_ascii=False).encode('utf-8')
        response = requests.post(self.__endpoint_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        answer = json.loads(response.text)["answer"]
        print("LLM Answer:", answer)
        print("-------------------------")
        return answer


if __name__ == "__main__":
    llm = ProxyMistralLLM(endpoint_url="http://81d3-34-118-241-70.ngrok-free.app/ask")
    ctx = MistralContext()
    ctx.add_user_message(entry="Who are you?")
    answer = llm.ask(context=ctx)
    print(answer)
