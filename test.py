from llm.mistral_llm import MistralLLM
from qa_constructor.mistral_qa_constructor import MistralQAConstructor
from qa_constructor.mistral_qa_constructor_advanced import MistralQAConstructorAdvanced
from utils.enums import MistralTypes

# llm = MistralLLM(mistral_type=MistralTypes.GPTQ_8bit)
#
# qa_constructor = MistralQAConstructor()
# qa_constructor.create_qa_pairs()

from ctransformers import AutoModelForCausalLM

qa_constructor = MistralQAConstructorAdvanced(ready_docs_path="./storage/docs/docs_2023-11-30_13-54-03.pkl", proxy_llm_url="http://f3e7-34-125-105-188.ngrok-free.app/ask", source_docs_path="./storage/sources/uni-alt")
qa_constructor.create_qa_pairs(save_questions=True)
#qa_constructor.answer_questions()

from ctransformers import AutoModelForCausalLM