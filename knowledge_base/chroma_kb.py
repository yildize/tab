from sentence_transformers import SentenceTransformer

from knowledge_base.knowledge_base import KnowledgeBase
from langchain.vectorstores import Chroma
from langchain.retrievers import SVMRetriever
from utils.protocols import Embedder
from typing import Union, List
from utils.protocols import Doc
from langchain.embeddings import HuggingFaceEmbeddings


class ChromaKB(KnowledgeBase):

    def __init__(self, embedder:Union[Embedder, HuggingFaceEmbeddings], docs_path:str):
        super().__init__(embedder=embedder, docs_path=docs_path)
        self.svm_retriever = SVMRetriever.from_documents(self.docs, self.embedder)

    def search(self, q, method, method_kwargs):
        docs = None
        if method == "KNN":
            docs: List[Doc] = self.db.similarity_search(q)
        elif method == "SVM":
            docs: List[Doc] = self.svm_retriever.get_relevant_documents(q)
        return docs

    def _construct_storage(self):
        """ Returned db will be catched by self.db"""
        db = Chroma.from_documents(documents=self.docs, embedding=self.embedder)
        return db