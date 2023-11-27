from llm.contexts.mistral_context import MistralContext

class Contexts:
    def __init__(self):
        self.mistral_test = self.__mistral_test_context()
        self.mistral_q_derive = self.__mistral_q_derive()
        self.mistral_a_derive = self.__mistral_a_derive()

    def __mistral_test_context(self) -> MistralContext:
        context = MistralContext()
        context.add_user_message("Hello there, tell me about yourself.")
        return context

    def __mistral_q_derive(self) -> MistralContext:
        context = MistralContext()
        context.add_user_message(entry="I will feed you with some company-private document pages. Those documents are explaining company-specific procedures. My purpose is to build a "
                                       " question-answer database using those documents and help company employees to find quick answers to their practical questions regarding those documents. "
                                       " For example user/employee can wonder what to do or how to do it in a specific condition by asking simple questions. What I want you to do is "
                                       "extract/derive potential questions that might be asked by users/employees regarding the document page I will be providing. Note that, users "
                                       "will be unaware of the exact documents or previous questions so they can't ask questions regarding specifics of a document, they are more likely to ask more "
                                       "general, insightful and practical questions. For example a user question can't contain phrases like 'this document', 'previous question' and so on. Finally, "
                                       "if a content doesn't seem to be very rich or informative don't push yourself to extract some questions. ")
        context.add_assistant_message(entry="I have read your instruction very carefully, and I totally understood what to do. Give me the content so I can derive potential user/employee questions "
                                            "using only the provided content.")
        context.add_user_message(entry=f"...") # Great! Here is your context:\n{context}
        return context

    # def __mistral_q_derive(self) -> MistralContext:
    #     context = MistralContext()
    #     context.add_user_message(entry="I need you to help me on a subject. I will build a system to help users find quick answers to their questions "
    #                                    "regarding multiple different subject PDFs. The way I will do it is to loop through all pages of each document and derive "
    #                                    "practical/useful questions from each document. Later I will map arbitrary user questions to those derived questions and "
    #                                    "quickly retrieve the paired correct answer for it. Now I will start providing you with random page contents from documents, "
    #                                    "please derive useful/practical questions ONLY using the content provided. Those questions should be insightful questions imitating "
    #                                    "user questions who is unaware of the document, the content or previous questions. Each question should be unique, independent and "
    #                                    "stand-alone. Questions can be both broadscale or narrowscale as long as they are insightful and practical.")
    #     context.add_assistant_message(entry="""I have read your instruction very carefully, and I totally understood what to do. Give me the content so I can derive those questions.""")
    #     context.add_user_message(entry=f"...") # Great! Here is your context:\n{context}
    #     return context

    # def __mistral_q_derive(self) -> MistralContext:
    #     context = MistralContext()
    #     context.add_user_message(entry="I will provide you with a content and I want you to derive core practical/insightful questions from this document. Those questions should imitate "
    #                                    "questions that a human being who wants to learn about provided content. Questions should be independent, stand alone, comprehesive and informative. ")
    #     context.add_assistant_message(entry="""I have read your instruction very carefully, and I totally understood what to do. Give me the content so I can derive those questions.""")
    #     context.add_user_message(entry=f"...") # Great! Here is your context:\n{context}
    #     return context

    def __mistral_a_derive(self) -> MistralContext:
        context = MistralContext()
        context.add_user_message("...")
        return context

    def __mistral_q_derive2(self) -> MistralContext:
        context = MistralContext()
        context.add_user_message(entry="""I will provide you a page content taken from a very long PDF. I want you to very carefully read this page content and derive SPECIFIC insightful/practical questions
        and their CORRECT answers using ONLY the provided page content. Those questions should imitate user questions who wants to get familiar with the provided content. And the answers should be
        broad and clear as much as possible. You will only use the information given in the context. Did you understand?""")
        context.add_assistant_message(entry="""I have read your instruction very carefully, and I totally understood what to do. Now give me the page content.""")
        context.add_user_message(entry=f"...") # Great! Here is your context:\n{context}
        return context


ready_ctxs = Contexts()
