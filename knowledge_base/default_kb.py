from knowledge_base.knowledge_base import CustomKnowledgeBase
from typing import Union, List
from utils.protocols import Doc
import faiss
from knowledge_base.embedders import SetenceTransformerEmbedder


class DefaultKnowledgeBase(CustomKnowledgeBase):
    db: faiss.IndexFlatIP
    embedder: SetenceTransformerEmbedder

    def __init__(self, docs: Union[str, List[Doc]], embedder_name:str):
        super().__init__(docs=docs, embedder=SetenceTransformerEmbedder(embedder_name=embedder_name))

    def _construct_storage(self):
        embeddings = self.embedder([doc.page_content for doc in self.docs])
        faiss.normalize_L2(embeddings)
        db = faiss.IndexFlatIP(self.embedder.embedding_dim)
        db.add(embeddings)
        return db

    def search(self, q, k=3):
        query_embedding = self.embedder(q)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.db.search(x=query_embedding, k=k)
        res_docs = []
        for index, dist in zip(indices[0], distances[0]):
            similar_doc = self.docs[index]
            similar_doc.metadata["retrieval_info"] = {"q":q, "dist":dist, "token_len": self.embedder.len_required_tokens(similar_doc.page_content)}
            res_docs.append(self.docs[index])
        return res_docs