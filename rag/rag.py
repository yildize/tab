from knowledge_base.default_kb import DefaultKnowledgeBase
from typing import List

from llm.contexts.mistral_context import MistralContext
from llm.mistral_llm import MistralLLM
from utils.enums import MistralTypes
from utils.protocols import Doc
import os

class DefaultRetrievalAugmentedGenerator:
    def __init__(self, docs:List[Doc], llm=None):
        self._docs = docs
        self._llm = MistralLLM(mistral_type=MistralTypes.GPTQ_4bit) if llm is None else llm
        self._kb = DefaultKnowledgeBase(docs=docs, embedder_name="msmarco-MiniLM-L-6-v3")#embedder_name="all-mpnet-base-v2")

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
            #retrieved_content += f"Source{i}:{os.path.basename(source)}\nContent{i}:{content}\n\n-----------\n" # f"Content{i}:{content}\n-----------\n" #
            #retrieved_content +=  f"{i+1}. {content}\n"
            retrieved_content += f"--- Content {i + 1} ---\n\n{content}\n\n"
        context = MistralContext()

#         context.add_user_message(entry=f""""Question: [{question}]\n\n Content Sources:\n[{retrieved_content}]\n\n. Please give a clear and concise answer to the question using the above content sources.
# PAY ATTENTION: If answer is not found on the Content Sources, ONLY ANSWER: 'Sorry, I don't know the answer.' """)

        context.add_user_message(entry=f"{question}\n\n"
                                   f"Carefully read the following contents, and give a clear and concise answer the above question accordingly. Answer can be found inside a single content or might require a synthesis of multiple contents. Here are the contents:\n\n{retrieved_content}")


        # context.add_user_message(
        #     entry=f"Assume, your name is TAB, you are an helpful and kind Information Management Assistant for Hacettepe University Computer Engineering Department."
        #           f"Your job is to help students by answering their questions utilizing provided page contents"
        #           f"I want you to give a clear and concise answer to the student question utilizing the provided page contents.\n\n"
        #           f"Do not directly refer to the page in your answer ('do not use phrases like according to the provided content'. "
        #           f"Finally, If you don't know the answer to the question ONLY respond:'Sorry, I don't know the answer.' "
        #           f"Here is the user question:\n[{question}]'''\n\nHere is the content:\n\n[{retrieved_content}]\n\n")
        return context

        # context.add_user_message(entry=f""""Question: {question}\n\n Content Sources:\n{retrieved_content}\n. Please give a clear and concise answer to the question using the above content sources.
        # PAY ATTENTION: If the content is not sufficient to answer the question, please ONLY ANSWER: 'Sorry, I don't know the answer.' """)

