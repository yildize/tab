from knowledge_base.default_kb import DefaultKnowledgeBase
from typing import List

from llm.contexts.mistral_context import MistralContext
from llm.mistral_llm import MistralLLM
from utils.enums import MistralTypes
from utils.protocols import Doc


class DefaultRetrievalAugmentedGenerator:
    def __init__(self, docs:List[Doc]):
        self._docs = docs
        self._llm = MistralLLM(mistral_type=MistralTypes.GPTQ_4bit)
        self._kb = DefaultKnowledgeBase(docs=docs, embedder_name="all-mpnet-base-v2")

    def ask(self, question:str):
        related_docs = self._kb.search(q=question, k=5)
        #concatenate related docs accordingly obtain the required llm context
        context = self.__prepare_retrieved_content(related_docs=related_docs, question=question)
        #ask question to the llm utilizing the retrieved context
        answer = self._llm.ask(context=context)
        return answer

    def __prepare_retrieved_content(self, related_docs: List[Doc], question:str):
        retrieved_content = ""
        for i,doc in enumerate(related_docs):
            source = doc.metadata["source"]
            content = doc.page_content
            retrieved_content += f"Source{i}:{source}\nContent{i}:{content}\n\n-----------\n"

        context = MistralContext()
        context.add_user_message(entry=f"Please answer the following user question utilizing the content provided below. If the content is not sufficient to answer this question, please"
                                       f"answer, 'Sorry, I could not find the answer in my knowledge base.'\n\nHere is the question:{question}\n\nHere is the content:{retrieved_content}.")
        return context





