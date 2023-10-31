from knowledge_base.default_kb import DefaultKnowledgeBase
from llm.contexts.mistral_context import MistralContext
from llm.mistral_llm import MistralLLM
from splitters.pdf_splitter import PdfSplitter
import re

class MistralQAConstructor:
    class QAPair:
        def __init__(self, q, a, metadata):
            self.q, self.a, self.metadata = q, a, metadata
    def __init__(self):

        self.pdf_splitter = PdfSplitter(local_src_path="./storage/sources/antalya-guide.pdf")
        self.__splits = self.pdf_splitter.split()
        self.__page_docs = self.pdf_splitter.split(pages_only=True)

        self.llm = MistralLLM()
        self.kb = DefaultKnowledgeBase(docs=self.__splits, embedder_name="all-mpnet-base-v2")
        self.llm_contenxt = self.__set_contenxt()
        self.qa_pairs =[]

    def create_qa_pairs(self):
        for page_doc in self.__page_docs:
            self.llm_contenxt.update_last_message_content(entry=f"Great! Here is your page content:\n{page_doc.page_content}")
            answer = self.llm.ask(context=self.llm_contenxt)
            print("answer:", answer)
            extracted_qas = self.__extract_qa_pairs(answer)
            self.qa_pairs.append(extracted_qas)
            print(f"Total of {len(extracted_qas)} extracted.")

    def __extract_qa_pairs(self, text):
        # Split based on question starts and "Answer: " keyword
        parts = re.split(r'\d+\.\s|Answer:\s', text)

        # Filter out empty strings
        parts = [part.strip() for part in parts if part.strip()]

        # Group questions and answers in pairs
        qa_pairs = [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]

        return qa_pairs

    def __set_contenxt(self):
        context = MistralContext()
        context.add_user_message(entry="""I will provide you a page content taken from a very long PDF. I want you to very carefully read this page content and derive SPECIFIC insightful/practical questions (at least three and more
        when you think it is necessary) and their CORRECT answers using ONLY the provided page content. The questions you've derived should be very descriptive and specific, avoid deriving general questions also those questions should be
        key questions that a human being can really utilize and corresponding answers MUST be CORRECT! You will only use the information given in the context. Did you understand?""")
        context.add_assistant_message(entry="""I have read your instruction very carefully, and I totally understood what to do. Now give me the page content so I can derive those specific insightful/practical/useful questions and the correct
        answers by very carefully reading this page content.""")
        context.add_user_message(entry=f"...") # Great! Here is your context:\n{context}
        return context