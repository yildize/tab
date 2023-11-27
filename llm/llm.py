import os.path
from abc import ABC, abstractmethod
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from utils.utils import ROOT_PATH


class LLM(ABC):

    def __init__(self, model_name:str):
        self._cache_dir = os.path.join(ROOT_PATH, "storage", "llms")
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model_name = model_name
        self.model, self.tokenizer = self._construct_model()
        self._configure_model()

    def _construct_model(self):
        model = AutoModelForCausalLM.from_pretrained(self._model_name, device_map=self._device, trust_remote_code=False,
                                                     revision="main", cache_dir=self._cache_dir)
        tokenizer = AutoTokenizer.from_pretrained(self._model_name, use_fast=True, cache_dir=self._cache_dir)
        return model, tokenizer

    def _configure_model(self):
        """ Will be called just after model constructions can be used to provide initial configurations"""
        ...

    @abstractmethod
    def ask(self, *args, **kwargs):
        ...


