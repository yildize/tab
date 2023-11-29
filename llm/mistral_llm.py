import json

from llm.contexts.mistral_context import MistralContext
from llm.llm import LLM
import os

from utils.enums import MistralTypes
from utils.utils import ROOT_PATH
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from ctransformers import AutoModelForCausalLM as CAutoModelForCausalLM


class MistralLLM(LLM):
    """ This class is a wrapper around MistralLLM."""

    def __init__(self, mistral_type: MistralTypes = MistralTypes.GPTQ_4bit):
        self._mistral_type = mistral_type
        model_path = {MistralTypes.GPTQ_4bit: os.path.join(ROOT_PATH, "storage", "llms",'mistral-gptq-4bit-32g-actorder_True'),
                      MistralTypes.GPTQ_8bit: os.path.join(ROOT_PATH, "storage", "llms",'mistral-gptq-8bit-128g-actorder_True'),
                      MistralTypes.GGUF_Q5: "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                      MistralTypes.GGUF_Q6: "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
                      }[mistral_type]
        super().__init__(model_name=model_path)

    def ask(self, context: MistralContext) -> str:
        model_inputs = self.tokenizer.apply_chat_template(context.messages, return_tensors="pt").to(self._device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=2048, do_sample=False).cpu()
        decoded = self.tokenizer.batch_decode(generated_ids)
        return self.__get_last_response(decoded[0])

    def _construct_model(self):
        if self._mistral_type.name.startswith("GGUF"):
            model_file = "mistral-7b-instruct-v0.1.Q5_K_M.gguf" if self._mistral_type == MistralTypes.GGUF_Q5 else "mistral-7b-instruct-v0.1.Q6_K.gguf"
            model = CAutoModelForCausalLM.from_pretrained(self._model_name, model_file=model_file, max_new_tokens=2048, context_length=8000, model_type="mistral", gpu_layers=50, cache_dir=self._cache_dir)
            # Use regular tokenizer to use apply_chat_template method
            tokenizer = AutoTokenizer.from_pretrained(os.path.join(ROOT_PATH, "storage", "llms", 'mistral-gptq-4bit-32g-actorder_True'), use_fast=True, cache_dir=self._cache_dir)
        else:
            model = AutoModelForCausalLM.from_pretrained(self._model_name, device_map=self._device, trust_remote_code=False,
                                                         revision="main", cache_dir=self._cache_dir)
            tokenizer = AutoTokenizer.from_pretrained(self._model_name, use_fast=True, cache_dir=self._cache_dir)
        return model, tokenizer

    @staticmethod
    def __get_last_response(full_text):
        inst_end_index = full_text.rfind('[/INST]')
        answer = full_text[inst_end_index + len('[/INST]'):].strip()
        if answer.endswith("</s>"): answer = answer[:-len("</s>")]
        return answer
