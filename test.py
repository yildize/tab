from llm.mistral_llm import MistralLLM
from qa_constructor.mistral_qa_constructor import MistralQAConstructor
from qa_constructor.mistral_qa_constructor_advanced import MistralQAConstructorAdvanced
from utils.enums import MistralTypes

# llm = MistralLLM(mistral_type=MistralTypes.GPTQ_8bit)
#
# qa_constructor = MistralQAConstructor()
# qa_constructor.create_qa_pairs()


qa_constructor = MistralQAConstructorAdvanced(proxy_llm_url="http://31ec-34-91-219-175.ngrok-free.app/ask", source_docs_path="./storage/sources/uni-alt", ready_docs_path="./storage/docs/ready_docs.pkl")
qa_constructor.create_qa_pairs(save_questions=True)

from ctransformers import AutoModelForCausalLM