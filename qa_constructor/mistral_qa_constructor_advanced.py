from typing import List

from knowledge_base.default_kb import DefaultKnowledgeBase
from llm.contexts.mistral_context import MistralContext
from llm.contexts.ready_to_use_contexts import ready_ctxs
from llm.mistral_llm import MistralLLM
from splitters.pdf_splitter import PdfSplitter
import re

from utils.protocols import Doc
from utils.enums import MistralTypes
from utils.utils import Question, QAS, QAPair
from datetime import datetime
import time


class MistralQAConstructorAdvanced:

    class QAPair:
        def __init__(self, q, a, metadata):
            self.q, self.a, self.metadata = q, a, metadata

    def __init__(self):
        self.llm = MistralLLM(mistral_type=MistralTypes.GPTQ_4bit)

        # Obtain the pages with index and summary:
        self.pdf_splitter = PdfSplitter(local_src_path="./storage/sources/tsps", chunk_size=1000, chunk_overlap=0)
        self.__page_docs = self.pdf_splitter.split(load_only=True, add_doc_index=True)
        self.__add_summary_to_pages()

        # Now obtain different chunk_sized splits to increase accuracy:
        splits1= self.pdf_splitter.split(docs=self.__page_docs)
        splits2 = PdfSplitter(local_src_path="./storage/sources/tsps", chunk_size=500, chunk_overlap=100).split(docs=self.__page_docs)
        splits3 = PdfSplitter(local_src_path="./storage/sources/tsps", chunk_size=250, chunk_overlap=100).split(docs=self.__page_docs)
        splits4 = PdfSplitter(local_src_path="./storage/sources/tsps", chunk_size=250, chunk_overlap=100).split(docs=self.__page_docs)

        # Finally obtain a List[Doc] consisting of page_summaries:
        summary_docs = self.__obtain_summary_docs()

        # Obtain a single split list:
        self.__splits = splits1 + splits2 + splits3 + splits4 + summary_docs

        # Now prepare a knowledge base with the constructed splits
        self.kb = DefaultKnowledgeBase(docs=self.__splits, embedder_name="msmarco-MiniLM-L-6-v3") #  # all-mpnet-base-v2

        self._questions: List[Question] = []
        self.qa_pairs = QAS()
        self.t_check_point = time.time()


    def create_qa_pairs(self):
        self.__create_questions()
        self.__answer_questions()
        self.qa_pairs.save_to_json(f"./storage/extracted_questions/qas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}")

    def __add_summary_to_pages(self) -> None:
        """ This method adds a summary for each page, later will be used for indexing."""
        previous_page_summary = "No summary found."
        for page_doc in self.__page_docs:
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

    def __obtain_summary_docs(self) -> List[Doc]:
        summary_docs = []
        for page in self.__page_docs:
            # First deep copy the page, assuming it is a Langchain Document object
            page = page.copy(deep=True)
            # Replace page_content with the page_summary:
            page.page_content = page.metadata["page_summary"]
            summary_docs.append(page)
        return summary_docs

    def __get_related_pages(self, question:str, max_page_num=7) -> List[Doc]:
        """ This method will return the list of page_docs related to the question."""
        similar_docs = self.kb.search(q=question, k=20)
        docs_indexes = set()
        for doc in similar_docs:
            docs_indexes.add(doc.metadata["doc_index"])
            if len(docs_indexes) >= max_page_num: break

        related_page_docs = [self.__page_docs[doc_index] for doc_index in docs_indexes]

        return related_page_docs

    def __create_questions(self):
        # ready question derivation context
        ctx = MistralContext()
        ctx.add_user_message(entry="...")
        for i,page_doc in enumerate(self.__page_docs):
            # update ctx with page_doc.content
            ctx.update_last_message_content(entry=f"Based on the following page summary and content, please generate a comprehensive list of useful/practical "
                                                  f"questions. These questions should mimic those that might be asked by a student or teacher unfamiliar "
                                                  f"with the document, focusing on practical and significant aspects.\n\n"
                                                  f"Here is the page summary: [{page_doc.metadata['page_summary']}]\n\n"
                                                  f"Here is the page content: [{page_doc.page_content}]")
            # ask for question derivation to llm
            llm_answer = self.llm.ask(context=ctx)
            # parse answer and obtain questions
            qs_str = self.__parse_questions(llm_answer)
            # add questions to the storage (each question will have the question, metadata, and the page_doc itself)
            for q in qs_str:
                self._questions.append(Question(q=q,doc=page_doc))
                print("Extracted question: ", q)
            print(f"Page {i+1}/{len(self.__page_docs)} is examined in {time.time()-self.t_check_point:.2f} seconds. {len(qs_str)} questions derived. Now we have in total of {len(self._questions)} questions derived.")
            print("#######################################################################")
            self.t_check_point = time.time()

    def __parse_questions(self, llm_answer):
        # This pattern matches strings that start with a number, followed by a period and a space, and end with a question mark
        pattern = re.compile(r'^(\d+)\.\s(.*\?)', re.MULTILINE)

        questions = []
        lines = llm_answer.split('\n')

        for line in lines:
            match = pattern.match(line)
            if match:
                # The second group contains the question
                questions.append(match.group(2))
            elif line.strip():  # Only warn if the line isn't just whitespace
                # If the line does not match the pattern, warn the user
                print(f"Warning: The line '{line}' is not in the expected format. Answer: {llm_answer}")

        return questions

    def __answer_questions(self):
        # ready question answering context
        ctx = MistralContext()
        ctx.add_user_message(entry="...")
        for i,question in enumerate(self._questions):
            # update ctx with string question and the doc content
            related_docs = self.__get_related_pages(question=question.question,)
            pages_content = ""
            for i, doc in enumerate(related_docs):
                pages_content += f"Content {i+1}: [{doc.page_content}]\n\n"

            ctx.update_last_message_content(entry=f"I will provide you with pages of contents and a 'a user question'. "
                                                  f"I want you to clearly answer the user question utilizing the provided page contents.\n\n"
                                                  f"Here is the user question:\n[{question.question,}]'''\n\nHere is the content:\n\n{pages_content}")
            # ask for answer to llm
            llm_answer = self.llm.ask(context=ctx)
            # parse answer
            a_str = self.__parse_answer(llm_answer)
            # construct qa pairs (question, answer, metadata)
            self.qa_pairs.add_pair(QAPair(q=question.question, a=a_str, m=[page.metadata for page in pages_content]))
            print(f"{i+1}/{len(self._questions)} is answered it took {(time.time()-self.t_check_point):.2f} seconds.")
            self.t_check_point = time.time()

    def __parse_answer(self, llm_answer):
        return llm_answer
