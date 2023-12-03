import json

import requests
from typing import List
from utils.protocols import Doc
from utils.utils import DummyDoc


class ProxyKnowledgeBase:

    """ Proxy KB class to handle the knowledge base server."""
    def __init__(self, base_endpoint_url:str):
        self.base_endpoint_url = base_endpoint_url if base_endpoint_url.startswith("http") else f"http://{base_endpoint_url}"
        self.search_endpoint_url = self.base_endpoint_url+"/search"
        self.page_search_endpoint_url = self.base_endpoint_url +"/search_pages"

    def search(self, q, k=3) -> List[Doc]:
        #response = requests.post(self.endpoint_url, json={"content":q, "k":k})
        data = json.dumps({"content": q, "k":k}, ensure_ascii=False).encode('utf-8')
        response = requests.post(self.search_endpoint_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        doc_dicts = json.loads(response.text)["docs"]
        docs = [DummyDoc(page_content=doc_dict["page_content"], metadata=doc_dict["metadata"]) for doc_dict in doc_dicts]
        return docs

    def search_pages_with_cross_encoder(self, q, max_k=5, cross_encoder_input_k=20):
        data = json.dumps({"content": q, "k":max_k, "cross_encoder_input_k":cross_encoder_input_k}, ensure_ascii=False).encode('utf-8')
        response = requests.post(self.page_search_endpoint_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        doc_dicts = json.loads(response.text)["docs"]
        docs = [DummyDoc(page_content=doc_dict["page_content"], metadata=doc_dict["metadata"]) for doc_dict in doc_dicts]
        return docs


if __name__ == "__main__":
    kb = ProxyKnowledgeBase(endpoint_url="127.0.0.1:5000/search")
    docs = kb.search("Some random question", k=5)
    page_docs = kb.search_pages("Cemil")
    print(docs)