from typing import List

from knowledge_base.default_kb import DefaultKnowledgeBase
from llm.contexts.mistral_context import MistralContext
from llm.contexts.ready_to_use_contexts import ready_ctxs
from llm.mistral_llm import MistralLLM
from splitters.pdf_splitter import PdfSplitter
import re

from utils.enums import MistralTypes
from utils.utils import Question, QAS, QAPair
from datetime import datetime
import time


class MistralQAConstructor:

    class QAPair:
        def __init__(self, q, a, metadata):
            self.q, self.a, self.metadata = q, a, metadata

    def __init__(self):
        self.pdf_splitter = PdfSplitter(local_src_path="./storage/sources/tsps")
        self.__splits = self.pdf_splitter.split()
        self.__page_docs = self.pdf_splitter.split(load_only=True)

        self.llm = MistralLLM(mistral_type=MistralTypes.GPTQ_4bit)
        #self.kb = DefaultKnowledgeBase(docs=self.__splits, embedder_name="all-mpnet-base-v2")

        self._questions: List[Question] = []
        self.qa_pairs = QAS()
        self.t_check_point = time.time()

    def create_qa_pairs(self):
        self.__create_questions()
        self.__answer_questions()
        self.qa_pairs.save_to_json(f"./storage/extracted_questions/qas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}")

    def __create_questions(self):
        # ready question derivation context
        ctx =  ready_ctxs.mistral_q_derive
        for i,page_doc in enumerate(self.__page_docs):
            # update ctx with page_doc.content
            ctx.update_last_message_content(f"Great! Here is your content:\n\n{page_doc.page_content}")
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
        ctx = ready_ctxs.mistral_a_derive
        for i,question in enumerate(self._questions):
            # update ctx with string question and the doc content
            q_str, page_content, metadata = question.question, question.doc.page_content, question.doc.metadata
            #ctx.update_last_message_content(entry=f"I want you to answer the following question using the following content only. Here is the question:\n{q_str}\n\nHere is the content:\n\n{page_content}") #todo: fix
            ctx.update_last_message_content(entry=f"I will provide you with a 'company-specific content' and an 'employee/user question'. I want you to clearly answer the user question utilizing the provided company specific content.\n"
                                                  f"Here is the user question:\n'''{q_str}'''\n\nHere is the content:\n\n{page_content}")
            # ask for answer to llm
            llm_answer = self.llm.ask(context=ctx)
            # parse answer
            a_str = self.__parse_answer(llm_answer)
            # construct qa pairs (question, answer, metadata)
            self.qa_pairs.add_pair(QAPair(q=q_str, a=a_str, m=metadata))
            print(f"{i+1}/{len(self._questions)} is answered it took {(time.time()-self.t_check_point):.2f} seconds.")
            self.t_check_point = time.time()

    def __parse_answer(self, llm_answer):
        return llm_answer

    # def create_qa_pairs(self):
    #     ctx = ready_ctxs.mistral_q_derive2
    #     for page_doc in self.__page_docs:
    #         ctx.update_last_message_content(entry=f"Great! Here is your page content:\n{page_doc.page_content}")
    #         answer = self.llm.ask(context=ctx)
    #         print("answer:", answer)
    #         extracted_qas = self.__extract_qa_pairs(answer)
    #         self.qa_pairs.append(extracted_qas)
    #         print(f"Total of {len(extracted_qas)} extracted.")
    #     print("Finished")
    #     print("-------------------")

    # def __extract_qa_pairs(self, text):
    #     # Split based on question starts and "Answer: " keyword
    #     parts = re.split(r'\d+\.\s|Answer:\s', text)
    #
    #     # Filter out empty strings
    #     parts = [part.strip() for part in parts if part.strip()]
    #
    #     # Group questions and answers in pairs
    #     qa_pairs = [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]
    #
    #     return qa_pairs
