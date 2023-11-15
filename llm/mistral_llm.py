import json

from llm.contexts.mistral_context import MistralContext
from llm.llm import LLM
import os

from utils.enums import MistralTypes
from utils.utils import ROOT_PATH


class MistralLLM(LLM):

    def __init__(self, mistral_type:MistralTypes = MistralTypes.GPTQ_4bit):
        model_path = {MistralTypes.GPTQ_4bit:os.path.join(ROOT_PATH, "storage", "llms",'mistral-gptq-4bit-32g-actorder_True'),
                      MistralTypes.GPTQ_8bit:os.path.join(ROOT_PATH, "storage", "llms",'mistral-gptq-8bit-128g-actorder_True'),
                      MistralTypes.GGUF_Q6: os.path.join(ROOT_PATH, "storage", "llms",'mistral-7b-Q6-GGUF')
                      }[mistral_type]
        super().__init__(model_name=model_path)

    def ask(self, context: MistralContext) -> str:
        model_inputs = self.tokenizer.apply_chat_template(context.messages, return_tensors="pt").to(self._device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=2048).cpu()
        decoded = self.tokenizer.batch_decode(generated_ids)
        return self.__get_last_response(decoded[0])

    @staticmethod
    def __get_last_response(full_text):
        inst_end_index = full_text.rfind('[/INST]')
        answer = full_text[inst_end_index + len('[/INST]'):].strip()
        if answer.endswith("</s>"): answer = answer[:-len("</s>")]
        return answer

