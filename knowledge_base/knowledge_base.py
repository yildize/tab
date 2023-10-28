import pickle
from abc import ABC, abstractmethod

from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from utils.protocols import Embedder
from langchain.vectorstores import Chroma
from typing import Union, List
from utils.protocols import Doc
from utils.utils import ROOT_PATH
import os


class KnowledgeBase(ABC):

    def __init__(self, embedder: Union[Embedder, HuggingFaceEmbeddings], docs_path:str):
        self.embedder = embedder
        self.docs: List[Doc] = self.__load_docs(docs_path=docs_path)
        self.__check_chunk_length()
        self.db = self._construct_storage()

    def __load_docs(self, docs_path:str):
        if not os.path.isabs(docs_path): docs_path = os.path.join(ROOT_PATH, docs_path)
        with open(docs_path, 'rb') as file:
             return pickle.load(file)

    def __check_chunk_length(self):
        for doc in self.docs:
            tokenized_length = len(self.embedder.client.tokenizer.tokenize(doc.page_content))
            if tokenized_length > self.embedder.client.max_seq_length:
                print(f"Max seq len is {self.embedder.max_seq_length} but a doc with content len {tokenized_length} is found!")

    @abstractmethod
    def _construct_storage(self):
        ...

    @abstractmethod
    def search(self, q, method, method_kwargs):
        ...
