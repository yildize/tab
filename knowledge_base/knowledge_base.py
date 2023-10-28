import pickle
from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer
from utils.protocols import Embedder
from langchain.vectorstores import Chroma
from typing import List
from utils.protocols import Doc
from utils.utils import ROOT_PATH
import os


class KnowledgeBase(ABC):

    def __init__(self, embedder: Embedder, docs_path:str):
        self.embedder = embedder
        self.docs: List[Doc] = self.__load_docs(docs_path=docs_path)
        self.storage = self.construct_storage()


    def __load_docs(self, docs_path:str):
        if not os.path.isabs(docs_path): docs_path = os.path.join(ROOT_PATH, docs_path)
        with open(docs_path, 'rb') as file:
             return pickle.load(file)

    @abstractmethod
    def construct_storage(self):
        ...

    @abstractmethod
    def query(self, q, strategy):
        ...
