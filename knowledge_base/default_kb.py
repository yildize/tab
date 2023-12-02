import os
from knowledge_base.knowledge_base import CustomKnowledgeBase
from typing import Union, List, Optional
from utils.protocols import Doc
import faiss
from numpy import np
from knowledge_base.embedders import SetenceTransformerEmbedder


class DefaultKnowledgeBase(CustomKnowledgeBase):
    db: faiss.IndexFlatIP
    embedder: SetenceTransformerEmbedder

    def __init__(self, docs: Union[str, List[Doc]], embedder_name:str, cross_encoder_name: Optional[str]=None):
        super().__init__(docs=docs, embedder=SetenceTransformerEmbedder(embedder_name=embedder_name), cross_encoder_name=cross_encoder_name)

    def _construct_storage(self):
        embeddings = self.embedder([doc.page_content for doc in self.docs])
        faiss.normalize_L2(embeddings)
        db = faiss.IndexFlatIP(self.embedder.embedding_dim)
        db.add(embeddings)
        return db

    def search(self, q, k=3) -> List[Doc]:
        query_embedding = self.embedder(q)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.db.search(x=query_embedding, k=k)
        res_docs = []
        for index, dist in zip(indices[0], distances[0]):
            # Deep copy to provide thread safety for multi-threadded usages.
            similar_doc = self.docs[index].copy(deep=True) # use copy.deepcopy(self.docs[index]) if it throws an error.
            similar_doc.metadata["retrieval_info"] = {"q": q, "dist": dist, "token_len": self.embedder.len_required_tokens(similar_doc.page_content)}
            res_docs.append(similar_doc)
        return res_docs

    def search_pages_with_cross_encoder(self, q, max_k=5, cross_encoder_input_k=20) -> List[Doc]:
        """ Note that for this search method, the number of the return documents can be lower than
        max_k when multiple chunks are from the same page. Also note that this method relies on
        docs having doc_index field inside their metadata."""
        # First retrieve similar chunks by regular kb search
        similar_docs = self.search(q=q, k=cross_encoder_input_k) # each doc is typically a chunk.
        # Now pass them to cross_encoder for finer similarity analysis. It will compare question to similar doc contents:
        scores = self.cross_encoder.predict([[q, doc.page_content] for doc in similar_docs])

        # Now only top k most related docs will be selected
        sorted_indices = np.argsort(-scores) # sort in a decreasing score order.
        docs_indexes = {} # stores the doc indexes of most similar docs and their scores.
        for i in sorted_indices:
            doc = similar_docs[i]
            if doc.metadata.get('doc_index') is None: raise AttributeError('search_pages_with_cross_encoder methods needs doc_index attribute for the docs in order to perform!')
            docs_indexes[doc.metadata["doc_index"]] = scores[i]
            if len(docs_indexes) >= max_k: break

        # Now extract and deep copy those most similar page-docs to thread-safely modify them:
        related_page_docs = []
        for doc_index, score in docs_indexes.items():
            doc = self.docs[doc_index].copy(deep=True)
            doc.metadata["retrieval_info"] = {"q": q, "dist": score} # I kept the key as dist even though it is not exactly a distance measure just too keep it compatible.
            related_page_docs.append(doc)

        return related_page_docs

