import os
import requests
import json
from transformers import AutoTokenizer
from utils.utils import ROOT_PATH

from llm.contexts.mistral_context import MistralContext


class ProxyWizardLLM:
    def __init__(self, endpoint_url: str):
        self.__endpoint_url = endpoint_url
        self.__tokenizer = AutoTokenizer.from_pretrained('TheBloke/Mistral-7B-Instruct-v0.1-GPTQ', use_fast=True, cache_dir=os.path.join(ROOT_PATH, "storage", "llms"))

    def ask(self, user_question:str) -> str:
        model_input_str = self._generate_prompt_single_turn(user_question=user_question)
        # Prepare the data as a dictionary and convert it to a JSON string
        data = json.dumps({"query": model_input_str}, ensure_ascii=False).encode('utf-8')
        response = requests.post(self.__endpoint_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        answer = json.loads(response.text)["answer"]
        print("LLM Answer:", answer)
        print("-------------------------")
        return answer

    def _generate_prompt_single_turn(self, user_question):
        """
        Generates the prompt for a single turn conversation with WizardLM.

        Parameters:
        user_question (str): The question asked by the user.

        Returns:
        str: The complete prompt for the WizardLM model.
        """
        prompt = f"A chat between a curious user and an artificial intelligence assistant. " \
             f"The assistant gives helpful, detailed, and polite answers to the user's questions. " \
             f"USER: {user_question} ASSISTANT: "
        return prompt


