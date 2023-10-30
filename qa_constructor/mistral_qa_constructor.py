from knowledge_base.default_kb import DefaultKnowledgeBase
from llm.contexts.mistral_context import MistralContext
from llm.mistral_llm import MistralLLM
from splitters.pdf_splitter import PdfSplitter


class MistralConstructor:
    def __init__(self, docs, ):

        self.pdf_splitter = PdfSplitter(local_src_path="./storage/sources/antalya-guide.pdf")
        #page_docs = self.pdf_splitter._load_logic()
        #splits = self.pdf_splitter.split(save=False)
        self.llm = MistralLLM()
        self.kb =  DefaultKnowledgeBase(docs=, embedder_name=)
        self.llm_contenxt = self.__set_contenxt()

    def create_qa_pairs(self):
        self.llm_contenxt.update_last_message_content(entry="...")
        answer = self.llm.ask(context=self.llm_contenxt)
        qa_pairs = self.__parse_answers(answer)

    def __parse_answers(self):
        ...


    def __set_contenxt(self):
        context = MistralContext()
        context.add_user_message(entry="""I will provide you a context taken from a PDF.
                                           I want you to very carefully read this context and derive insightful/practical questions (at least 3 and more when needed) and their correct answers using ONLY the context.
                                           The questions and answers you've derived should be the key questions that a human being can really utilize and corresponding answers must be correct!
                                           You will only use the information given in the context that I will provide. Did you understand?
                                           """)
        context.add_assistant_message(entry="I have read your instruction very carefully, and I totally understand what to do. "
                                            "Now give me the context so I can derive those insightful/practical/useful questions by very carefully reading this context.")
        context.add_user_message(entry=f"Great! Here is your context:\n{context}")
        return context