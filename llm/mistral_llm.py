import json

from llm.contexts.mistral_context import MistralContext
from llm.llm import LLM



class MistralLLM(LLM):

    def __init__(self):
        super().__init__(model_name='TheBloke/Mistral-7B-Instruct-v0.1-GPTQ')

    def ask(self, context: MistralContext) -> str:
        model_inputs = self.tokenizer.apply_chat_template(context.messages, return_tensors="pt").to(self._device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=1000).cpu()
        decoded = self.tokenizer.batch_decode(generated_ids)
        return self.__get_last_response(decoded[0])

    @staticmethod
    def __get_last_response(full_text):
        inst_end_index = full_text.rfind('[/INST]')
        return full_text[inst_end_index + len('[/INST]'):].strip()

