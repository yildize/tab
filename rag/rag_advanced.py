from knowledge_base.default_kb import DefaultKnowledgeBase
from typing import List

from llm.contexts.mistral_context import MistralContext
from llm.mistral_llm import MistralLLM
from proxies.proxy_kb import ProxyKnowledgeBase
from proxies.proxy_mistral_llm import ProxyMistralLLM
from rest_apis.rag.schemas import metadata_schema
from utils.enums import MistralTypes
from utils.protocols import Doc
import os

class RAGAdvanced:
    def __init__(self, llm:ProxyMistralLLM = None, kb:ProxyKnowledgeBase = None, search_pages=True):
        self._llm = llm
        self._kb = kb
        self._search_pages = search_pages
    def ask(self, question:str, k=5, cross_encoder_input_k=20):
        """ If search pages is True, k is used as max_k for cross encoder"""
        related_page_docs = self._kb.search_pages_with_cross_encoder(q=question, max_k=k, cross_encoder_input_k=cross_encoder_input_k) if self._search_pages else self._kb.search(q=question, k=k)
        page_contents_str = self.__combine_page_contents(related_page_docs=related_page_docs)
        context = self.__construct_mistral_context(q_str=question, page_contents=page_contents_str)
        answer = self._llm.ask(context=context)
        metadata = [metadata_schema.dump(page_doc.metadata) for page_doc in related_page_docs]
        return answer, metadata

    def __combine_page_contents(self, related_page_docs: List[Doc]) -> str:
        pages_content = ""
        for i, page_doc in enumerate(related_page_docs):
            pages_content += f"Content {i + 1}: [{page_doc.page_content}]\n\n"
        return pages_content

    def __construct_mistral_context(self, q_str:str, page_contents:str):

        ctx = MistralContext()
        ctx.add_user_message("Your name is TAB, you are an helpful Information Managament Assistant Bot. Your job is to correctly give clear and concise answers to user question based on provided contents.")
        ctx.add_assistant_message("I understand. My name is TAB. I will give a clear and concise answer to provided user question utilizing the provided contents.")
        ctx.add_user_message(f"Please answer the following user question:[{q_str}]\nutilizing following contents:\n{page_contents}\n\n"
                             f"If the answer is not found among the contents, ONLY answer: Sorry I could not find the answer in my knowledge base.")
        # ctx = MistralContext()
        # ctx.add_user_message("Hello, who are you?")
        # ctx.add_assistant_message("Hello there! I am TAB an helpful Information Managament Assistant Bot. My job is to correctly give clear and concise answers to your questions based on provided contents.")
        # ctx.add_user_message("Great! I have a question and some page contents. Can you answer my questions utilizing the contents I will be providing?")
        # ctx.add_assistant_message("Of course, with pleasure. Please give me your question and the contents.")
        # ctx.add_user_message(f"Here is the user question: [{q_str}]\nHere is your contents:\n{page_contents}\n\n"
        #                      f"If the answer is not found among the contents, ONLY answer: Sorry I could not find the answer in my knowledge base.")


        # ctx.add_user_message(entry=f"Assume, you are an helpful Information Management Assistant for Hacettepe University Computer Engineering Department. "
        #           #f"Your job is to help students by answering their questions utilizing provided page contents."
        #           f"I want you to give a clear and concise answer to the student question utilizing the provided contents.\n\n"
        #           f"Here is the user question:\n[{q_str}]'''\n\nHere is your contents:\n\n[{page_contents}]\n\n"
        #           f"If the answer is not found among the contents, ONLY answer: Sorry I could not find the answer in my knowledge base.")
        return ctx


if __name__ == "__main__":
    llm = ProxyMistralLLM(endpoint_url="http://a7fa-34-80-134-151.ngrok-free.app/ask")
    kb = ProxyKnowledgeBase(base_endpoint_url="127.0.0.1:5000")
    rag = RAGAdvanced(llm=llm, kb=kb)
    answer, metadata = rag.ask(question="Contact information of Cemil Zalluhoglu?", k=8, cross_encoder_input_k=100)
    print()