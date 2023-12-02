from llm.mistral_llm import MistralLLM
from qa_constructor.mistral_qa_constructor import MistralQAConstructor
from qa_constructor.mistral_qa_constructor_advanced import MistralQAConstructorAdvanced
from utils.enums import MistralTypes

# llm = MistralLLM(mistral_type=MistralTypes.GPTQ_8bit)
#
# qa_constructor = MistralQAConstructor()
# qa_constructor.create_qa_pairs()

qa_constructor = MistralQAConstructorAdvanced(derived_questions_path="./storage/extracted_questions/qs_uni.json",
                                              ready_docs_path="./storage/docs/docs_2023-11-30_13-54-03.pkl",
                                              proxy_llm_url="http://df53-34-87-139-234.ngrok.io/ask",
                                              source_docs_path="./storage/sources/uni-alt")
qa_constructor.answer_questions(start_index=551, save_in_every_nth=10)

