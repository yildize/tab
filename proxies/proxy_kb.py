import json

import requests
from typing import List

from dataclasses import dataclass
from utils.protocols import Doc


class ProxyKnowledgeBase:

    @dataclass
    class DummyDoc:
        page_content:str
        metadata: dict

    """ Proxy KB class to handle the knowledge base server."""
    def __init__(self, endpoint_url:str):
        self.endpoint_url = endpoint_url if endpoint_url.startswith("http") else f"http://{endpoint_url}"

    def search(self, q, k=3) -> List[Doc]:
        response = requests.post(self.endpoint_url, json={"content":q, "k":k})
        doc_dicts = json.loads(response.text)["docs"]
        docs = [self.DummyDoc(page_content=doc_dict["page_content"], metadata=doc_dict["metadata"]) for doc_dict in doc_dicts]
        return docs


if __name__ == "__main__":
    kb = ProxyKnowledgeBase(endpoint_url="127.0.0.1:5000/search")
    docs = kb.search("Some random question", k=5)
    print(docs)