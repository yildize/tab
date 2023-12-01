import json
import os
import numpy as np
import pickle
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter

from knowledge_base.default_kb import DefaultKnowledgeBase
from llm.contexts.mistral_context import MistralContext
from llm.contexts.ready_to_use_contexts import ready_ctxs
from llm.mistral_llm import MistralLLM
from proxies.proxy_mistral_llm import ProxyMistralLLM
from splitters.pdf_splitter import PdfSplitter
import re

from utils.protocols import Doc
from utils.enums import MistralTypes
from utils.utils import Question, QAS, QAPair, ROOT_PATH
from datetime import datetime
import time

from sentence_transformers import CrossEncoder


class MistralQAConstructorAdvanced:

    class QAPair:
        def __init__(self, q, a, metadata):
            self.q, self.a, self.metadata = q, a, metadata

    def __init__(self, derived_questions_path: str = None, proxy_llm_url:str = None, source_docs_path:str=None, ready_docs_path:str=None):
        self.source_docs_path = source_docs_path
        # Prepare the llm
        #self.llm = MistralLLM(mistral_type=MistralTypes.GPTQ_4bit)
        self.llm = ProxyMistralLLM(endpoint_url=proxy_llm_url)

        # Obtain the pages with index and summary:
        self.pdf_splitter = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=1000, chunk_overlap=0)
        if ready_docs_path:
            # todo: update splitter logic, if docs are already given I don't need to provide a source_docs_path to splitter since I won't need it.
            self.__page_docs = self.__load_docs(path=ready_docs_path)
        else:
            self.__page_docs = self.pdf_splitter.split(load_only=True, add_doc_index=True)
            self.__add_summary_to_pages()
            self.__save_docs()
        #self.__reformat_page_contents()

        # Prepare the storage items
        self._questions: List[str] = [] if derived_questions_path is None else self.__load_questions(path=derived_questions_path)
        self.qa_pairs = QAS()

        # Flags
        self.__questions_ready = True if derived_questions_path is not None else False
        self.__kb_configured = False

        # Just for debugging
        self.t_check_point = time.time()

    def __save_docs(self):
        path = f"./storage/docs/docs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.pkl')}"
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, 'wb') as file:
            pickle.dump(self.__page_docs, file)
    def __load_docs(self, path:str):
        with open(path, 'rb') as file:
            return pickle.load(file)

    def create_questions(self, save=True):
        # ready question derivation context
        ctx = MistralContext()
        ctx.add_user_message(entry="...")
        for i,page_doc in enumerate(self.__page_docs):
            # todo : wizard - mistral?
            ctx = ready_ctxs.advanced_q_derive_wizard(page_summary=page_doc.metadata["page_summary"], page_content=page_doc.page_content)
            llm_answer = self.llm.ask(context=ctx)
            qs_str = self.__parse_questions(llm_answer.strip())

            # For the current page derive extra questions on sub-chunks:
            # for chunk in self.__sub_pages(page_doc=page_doc):
            #     formatted_questions = "\n".join([f"{i+1}. {q_str}" for i, q_str in enumerate(qs_str)])
            #     ctx = ready_ctxs.advanced_sub_q_derive(page_summary=chunk.metadata["page_summary"], page_content=chunk.page_content, prev_questions=formatted_questions)
            #     llm_answer = self.llm.ask(context=ctx)
            #     qs_str += self.__parse_questions(llm_answer)

            # add questions to the storage (each question will have the question, metadata, and the page_doc itself)
            for q in qs_str:
                self._questions.append(q)
                print("Extracted question: ", q)
            print(f"Page {i+1}/{len(self.__page_docs)} is examined in {time.time()-self.t_check_point:.2f} seconds. {len(qs_str)} questions derived. Now we have in total of {len(self._questions)} questions derived.")
            print("#######################################################################")
            self.t_check_point = time.time()

        if save: self.__save_questions()
        self.__questions_ready = True

    def __sub_pages(self, page_doc):
        # First split the doc into small chunks
        pdf_splitter = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=600, chunk_overlap=100)
        splits = pdf_splitter.split(docs=[page_doc])
        for split_doc in splits:
            yield split_doc

    def answer_questions(self, save_in_every_nth:int=10):
        if not self.__questions_ready: raise Exception("You are trying to answer questions without deriving questions or feeding a pre-derived question path.")
        self.__configure_kb() # Configure the knowledge base for advanced answering.

        # ready question answering context
        ctx = MistralContext()
        ctx.add_user_message(entry="...")
        for qi,q_str in enumerate(self._questions):
            # update ctx with string question and the doc content
            related_pages = self.__get_related_pages(question=q_str)
            pages_content = ""
            for i, page_doc in enumerate(related_pages):
                pages_content += f"Content {i+1}: [{page_doc.page_content}]\n\n"

            ctx.update_last_message_content(entry=f"I will provide you with pages of contents and a 'a user question'. "
                                                  f"I want you to give a clear and concise answer to ONLY the user question utilizing the provided page contents.\n\n"
                                                  f"Here is the user question:\n[{q_str}]'''\n\nHere is the content:\n\n[{pages_content}]\n\n"
                                                  f"Only answer the question, keep your answer concise and direct!")
            # ask for answer to llm
            llm_answer = self.llm.ask(context=ctx)
            a_str = self.__parse_answer(llm_answer)
            # construct qa pairs
            self.qa_pairs.add_pair(QAPair(q=q_str, a=a_str, m=[page.metadata for page in related_pages]))
            print(f"{qi+1}/{len(self._questions)} is answered it took {(time.time()-self.t_check_point):.2f} seconds.")
            self.t_check_point = time.time()
            if qi+1%save_in_every_nth==0: self.qa_pairs.save_to_json(f"./storage/extracted_questions/qas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}")

    def create_qa_pairs(self, save_questions=True):
        self.create_questions(save=save_questions)
        self.answer_questions()
        self.qa_pairs.save_to_json(f"./storage/extracted_questions/qas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}")

    def __configure_kb(self):
        if self.__kb_configured: return

        # Now obtain different chunk_sized splits to increase accuracy:
        splits1 = self.pdf_splitter.split(docs=self.__page_docs)
        splits2 = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=500, chunk_overlap=100).split(docs=self.__page_docs)
        splits3 = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=250, chunk_overlap=50).split(docs=self.__page_docs)
        splits4 = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=100, chunk_overlap=0).split(docs=self.__page_docs)
        splits5 = PdfSplitter(local_src_path=self.source_docs_path, chunk_size=15, chunk_overlap=0).split(docs=self.__page_docs)

        # Finally obtain a List[Doc] consisting of page_summaries:
        summary_docs = self.__obtain_summary_docs()

        # Obtain a single split list:
        self.__splits = splits1 + splits2 + splits3 + splits4 + summary_docs # + splits5

        # Now prepare a knowledge base with the constructed splits
        self.kb = DefaultKnowledgeBase(docs=self.__splits, embedder_name="msmarco-MiniLM-L-6-v3") #  # all-mpnet-base-v2
        self.__kb_configured = True

        cache_dir = os.path.join(ROOT_PATH, "storage", "cross-encoders")
        self.cross_encoder = CrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", tokenizer_args = {'cache_dir': cache_dir}, automodel_args = {'cache_dir': cache_dir}, max_length=512)

    def __get_related_pages(self, question:str, max_page_num=5) -> List[Doc]:
        """ This method will return the list of page_docs most-related to the question."""
        similar_docs = self.kb.search(q=question, k=20)

        scores = self.cross_encoder.predict([[question, doc.page_content] for doc in similar_docs])
        sorted_indices = np.argsort(-scores)

        docs_indexes = set()
        for i in sorted_indices:
            doc = similar_docs[i]
            docs_indexes.add(doc.metadata["doc_index"])
            if len(docs_indexes) >= max_page_num: break

        related_page_docs = [self.__page_docs[doc_index] for doc_index in docs_indexes]
        return related_page_docs

    # def __reformat_page_contents(self) -> None:
    #     for page in self.__page_docs:
    #         ctx = MistralContext()
    #         ctx.add_user_message(entry=f"Please rewrite the following page content in a more formatted way. Keep the content as it is just "
    #                                    f"reformat it.\n\nHere is the content:\n[{page.page_content}]")
    #         new_page_content = self.llm.ask(context=ctx)
    #         # Replace page_content with the page_summary:
    #         page.page_content = new_page_content

    def __add_summary_to_pages(self) -> None:
        """ This method adds a summary for each page, later will be used for indexing."""
        previous_page_summary = "No summary found."
        for i, page_doc in enumerate(self.__page_docs):
            prompt = f"Based on the content provided, determine if it continues the topic from the previous summary or introduces a new subject. " \
                     f"Summarize the main theme or content of this page in a single, brief sentence, avoiding specific details. " \
                     f"The summary should be general and succinct, suitable for quick indexing.\n\n" \
                     f"Previous Page Summary: [{previous_page_summary}]\n\n" \
                     f"Current Page Content: [{page_doc.page_content}]"
            ctx = MistralContext()
            ctx.add_user_message(entry=prompt)
            page_summary = self.llm.ask(context=ctx)
            page_doc.metadata["page_summary"] = page_summary
            previous_page_summary = page_summary
            print(f"Summary of page {i}/{len(self.__page_docs)}")


    def __obtain_summary_docs(self) -> List[Doc]:
        summary_docs = []
        for page in self.__page_docs:
            # First deep copy the page, assuming it is a Langchain Document object
            page = page.copy(deep=True)
            # Replace page_content with the page_summary:
            page.page_content = page.metadata["page_summary"]
            summary_docs.append(page)
        return summary_docs

    # def __parse_questions(self, llm_answer):
    #     # This pattern matches strings that start with a number, followed by a period and a space, and end with a question mark
    #     pattern = re.compile(r'^(\d+)\.\s(.*\?)', re.MULTILINE)
    #
    #     questions = []
    #     lines = llm_answer.split('\n')
    #
    #     for line in lines:
    #         match = pattern.match(line)
    #         if match:
    #             # The second group contains the question
    #             questions.append(match.group(2))
    #         elif line.strip():  # Only warn if the line isn't just whitespace
    #             # If the line does not match the pattern, warn the user
    #             print(f"Warning: The line '{line}' is not in the expected format. Answer: {llm_answer}")
    #
    #     return questions

    def __parse_questions(self, llm_answer):
        pattern = r'(?i)\b(?:What|How|Can|Who|Is|Are).*?\?'
        questions = re.findall(pattern, llm_answer)
        return questions

    def __parse_answer(self, llm_answer):
        return llm_answer

    # def __save_questions(self):
    #     with open(f"./storage/extracted_questions/qs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}",
    #               "w") as file:
    #         json.dump(self._questions, file)

    def __save_questions(self):
        path = f"./storage/extracted_questions/qs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding='utf-8') as file:
            json.dump(self._questions, file, indent=4)

    def __load_questions(self, path:str):
        with open(path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        return questions

