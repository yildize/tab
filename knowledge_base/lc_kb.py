from typing import Union, List, Optional
import warnings

from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.vectorstore import VectorStore
from langchain.retrievers import SVMRetriever

from utils.protocols import Doc
from utils.enums import LCVectorStores
from utils.utils import load_docs


class LangchainKnowledgeBase:
    """ This class contains easy access and handle for Langchain Vector Databases. Since I don't find their
    documentation very clear, I will be using them as it is through this class. For custom knowledge base
    I will be utilizing other classes further decomposing and modifying the components."""
    kb: Union[VectorStore, SVMRetriever]

    def __init__(self, docs:Union[str, List[Doc]], embedding:Union[OpenAIEmbeddings, HuggingFaceEmbeddings], type:LCVectorStores):
        """
        docs: Can be either a string path (absolute or relative to project folder) or the list of docs itself.
        type: Supported vector store types.
        """

        # If a path is specified as docs let's load it:
        self.docs = load_docs(docs) if isinstance(docs, str) else docs
        self.embedding = embedding
        self.type = type

        if type is LCVectorStores.Chroma:
            self.kb = Chroma.from_documents(documents=docs, embedding=embedding)
        elif type is LCVectorStores.FAISS:
            self.kb = FAISS.from_documents(documents=docs, embedding=embedding)
        elif type is LCVectorStores.SVM_Retriever:
            self.kb = SVMRetriever.from_documents(documents=self.docs, embeddings=embedding)
        else:
            ValueError(f"type {type} is not currently supported. Please provide one of {[elm.name for elm in LCVectorStores]}")

    def search(self, query:str, k:Optional[int]=None, scores:bool=False):
        """
        query: the string or embeddings that you want to search for
        k: Number of Documents to return. Defaults to 4.
        scores: Whether you want the scores.
        """
        if self.type is LCVectorStores.SVM_Retriever: # if isinstance(self.kb, SVMRetriever)
            if not isinstance(query, str): ValueError("SVM retriever accepts string as query.")
            if k or scores: warnings.warn("Warning SVM Retriever does not care about k argument and scores")
            similar_docs = self.kb.get_relevant_documents(query=query,)
        else:
            if k is None: k =  4
            similar_docs = self.kb.similarity_search_with_relevance_scores(query=query, k=k) if scores else self.kb.similarity_search(query=query, k=k)

        return similar_docs

    def add_docs(self):
        self.kb.add_documents()





