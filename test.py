from llm.mistral_llm import MistralLLM
from qa_constructor.mistral_qa_constructor import MistralQAConstructor
from qa_constructor.mistral_qa_constructor_advanced import MistralQAConstructorAdvanced
from utils.enums import MistralTypes

# llm = MistralLLM(mistral_type=MistralTypes.GPTQ_8bit)
#
# qa_constructor = MistralQAConstructor()
# qa_constructor.create_qa_pairs()


qa_constructor = MistralQAConstructorAdvanced(proxy_llm_url="http://fd6f-34-125-191-106.ngrok-free.app/ask", source_docs_path="./storage/sources/uni-alt")
qa_constructor.create_qa_pairs(save_questions=True)

from ctransformers import AutoModelForCausalLM