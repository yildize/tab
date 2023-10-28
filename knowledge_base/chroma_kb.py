from knowledge_base.knowledge_base import KnowledgeBase
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class ChromaKB(KnowledgeBase):
    def __init__(self):
        super().__init__()

    def query(self, q, strategy):
        embeddings = self.embedder(q)
        search_results = strategy.search() # strategy will have access to db, embedder and embeddings

    def construct_storage(self):
        return Chroma.from_documents(documents=docs, embedding=self.embedder)