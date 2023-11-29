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

    def advanced_q_derive(self, page_summary, page_content) -> MistralContext:
        context = MistralContext()
        context.add_user_message(entry=f""""Generate questions that can be answered using the detailed content provided. These questions should be as if asked by students who have not seen the document. They need to be practical, insightful, and directly related to the information in the reference content. Avoid creating questions that imply knowledge of the document's structure or existence, as the students are unaware of it.

Summary for context: [{page_summary}]
Detailed content for question generation: [{page_content}]

Examples of suitable questions:

'What is the contact information for Harun Artuner?'
'What are Fuat AKAL's research areas?'
Examples of unsuitable questions:

'Who are the new faculty members introduced in this section?'
'Can you list all the research areas mentioned?'
Please create questions based on the reference content, considering the provided guidelines.""")
        return context

    def advanced_sub_q_derive(self, page_summary, page_content, prev_questions):
        context = MistralContext()
        context.add_user_message(entry=f""""Create new un-derived questions based on the content of a specific section of a PDF page. These questions should be answerable using only the section's content and formulated as if by students unfamiliar with the entire document. They should be practical, insightful, and appear as naturally occurring inquiries.

Only derive questions on subjects are previously not covered by the already derived questions! Do not derived same or similar questions to previously derived questions. Try to cover missed subjects.
Detailed section content for question generation: [{page_content}]
Already derived questions: [{prev_questions}]

Please generate relevant questions, considering the detailed content of the subpart and the guidelines provided.""")
        return context


    # # update ctx with page_doc.content
    # ctx.update_last_message_content(entry=f"I will provide you with a sub-page content and a short summary of what was the page that the sub-page is derived from was about. "
    #                                       f"Based on ONLY the following sub-page content, please generate a list of independent, stand-alone, focused/content-specific list of useful/practical questions.. "
    #                                       f"These questions should mimic those that might be asked by a student or teacher unfamiliar with the document, focusing on practical and significant aspects. "
    #                                       f"You CAN NOT ask questions like 'What is ... in this document?' or 'What is ... of the listed elements? "
    #                                       f"Derive questions as if you don't know the existence of the documents, just focus to the content.\n\n"
    #                                       f"Here is the page summary: [{page_doc.metadata['page_summary']}]\n\n"
    #                                       f"Here is the sub-page content: [{chunk.page_content}]\n\n"
    #                                       f"Here are some previously derived questions from the page: [{formatted_questions}]\n\n"
    #                                       f"Derive questions similar to those but possibly forgotten/missed focusing on the sub-page content. "
    #                                       f"If the  sub-page content already contains derived questions, use them as is.")

ready_ctxs = Contexts()
