import os.path
from abc import ABC, abstractmethod
import numpy as np
from typing import Union, List

import torch
from langchain.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

from utils.utils import ROOT_PATH


class Embedder:
    def __init__(self, embedder_name:str):
        self.embedder = self._construct_embedder(embedder_name)

    @abstractmethod
    def _construct_embedder(self, embedder_name:str) -> Union[SentenceTransformer, OpenAIEmbeddings]:
        ...

    @property
    @abstractmethod
    def max_seq_length(self)->int:
        """ Returns the max sequence length for the embedder."""
        return self.embedder.max_seq_length

    @property
    @abstractmethod
    def embedding_dim(self)->int:
        ...

    @abstractmethod
    def len_required_tokens(self, text:str)->int:
        """ Returns  the number of tokens required to represent the given text"""
        ...

    def text_exceeds_max_seq_len(self, text:str) -> bool:
        return False


    @abstractmethod
    def __call__(self, texts) -> np.ndarray:
        """ This is where the actual embedding operation happens """
        ...


class SetenceTransformerEmbedder(Embedder):

    embedder: SentenceTransformer

    def __init__(self, embedder_name:str):
        super().__init__(embedder_name=embedder_name)

    def _construct_embedder(self, embedder_name:str) -> Union[SentenceTransformer, OpenAIEmbeddings]:
        return SentenceTransformer(embedder_name, cache_folder=os.path.join(ROOT_PATH, "storage", "sentence-transformers")) # todo: DEVICE!!!

    @property
    def max_seq_length(self)->int:
        """ Returns the max sequence length for the embedder."""
        return self.embedder.max_seq_length

    @property
    def embedding_dim(self) -> int:
        return self.embedder.get_sentence_embedding_dimension()

    def len_required_tokens(self, text:str):
        """ Returns  the number of tokens required to represent the given text"""
        return len(self.embedder.tokenizer.tokenize(text))
        # len(model.tokenizer(text, return_tensors="pt")["input_ids"].shape[1]) would be more accurate

    def text_exceeds_max_seq_len(self, text:str) -> bool:
        return self.len_required_tokens(text=text) > self.max_seq_length

    def __call__(self, sentences:str | List[str], to_numpy=True) -> Union[np.ndarray, torch.Tensor]:
        """ This is where the actual embedding operation happens. Shape will be (num_sentences, embedding_dim)"""
        if isinstance(sentences, str): sentences = [sentences]
        return self.embedder.encode(sentences, convert_to_numpy=to_numpy)