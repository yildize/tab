from llm.mistral_llm import MistralLLM
from qa_constructor.mistral_qa_constructor import MistralQAConstructor
from utils.enums import MistralTypes

llm = MistralLLM(mistral_type=MistralTypes.GPTQ_8bit)

qa_constructor = MistralQAConstructor()
qa_constructor.create_qa_pairs()