import pickle
from abc import ABC, abstractmethod

import numpy
from langchain.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

from knowledge_base.embedders import Embedder
from langchain.vectorstores import Chroma
from typing import Union, List
from utils.protocols import Doc
from utils.utils import ROOT_PATH, load_docs
import os




class CustomKnowledgeBase(ABC):

    def __init__(self, docs:Union[str, List[Doc]], embedder:Embedder):
        # If a path is specified as docs let's load it:
        self.docs = load_docs(docs) if isinstance(docs, str) else docs
        self.embedder = embedder
        self._check_chunk_length()

        self.db = self._construct_storage()

    def _check_chunk_length(self):
        for doc in self.docs:
            if self.embedder.text_exceeds_max_seq_len(doc.page_content):
                print(f"Max seq len is {self.embedder.max_seq_length} but a doc with content len {self.embedder.len_required_tokens(doc.page_content)} is found!")

    @abstractmethod
    def _construct_storage(self):
        ...

    @abstractmethod
    def search(self, *args, **kwargs) -> List[Doc]:
        ...
