import json

import requests
from typing import List
from utils.protocols import Doc
from utils.utils import DummyDoc


class ProxyRAG:

    """ Proxy KB class to handle the knowledge base server."""
    def __init__(self, endpoint_url:str):
        self.endpoint_url = endpoint_url if endpoint_url.startswith("http") else f"http://{endpoint_url}"

    def ask(self, question:str, k:int=5, cross_encoder_input_k=20) -> str:
        if len(question) > 1000: return "Your question is too long! Please ask shorter questions.", []
        data = json.dumps({"question": question, "k":k, "cross_encoder_input_k":cross_encoder_input_k}, ensure_ascii=False).encode('utf-8')
        response = requests.post(self.endpoint_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        answer = json.loads(response.text)["answer"]
        metadata = json.loads(response.text)["metadata"]
        return answer, metadata


if __name__ == "__main__":
    rag = ProxyRAG(endpoint_url="127.0.0.1:5001/ask")
    answer, metadata = rag.ask(question="Contact information of Mehmet Önder Efe?", k=7, cross_encoder_input_k=50)
    print(answer)