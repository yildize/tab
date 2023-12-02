import os
from knowledge_base.knowledge_base import CustomKnowledgeBase
from typing import Union, List, Optional, Dict, Tuple
from utils.protocols import Doc
import faiss
import numpy as np
from knowledge_base.embedders import SetenceTransformerEmbedder
import torch

class DefaultKnowledgeBase(CustomKnowledgeBase):
    db: faiss.IndexFlatIP
    embedder: SetenceTransformerEmbedder

    def __init__(self, docs: Union[str, List[Doc]], embedder_name:str, cross_encoder_name: Optional[str]=None, page_docs:Optional[Union[str, List[Doc]]]=None):
        """Here docs represent the docs to be embedded, typically they are chunk docs since sentence embedders
        have limited context sized. But for some cases, especially for cross-embedder search case, I will
        be utilizing page docs as well, therefore kb will be expecting those as a separate argument."""
        super().__init__(docs=docs, embedder=SetenceTransformerEmbedder(embedder_name=embedder_name), cross_encoder_name=cross_encoder_name, page_docs=page_docs)

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
        if self.page_docs is None: raise AttributeError("To use search_pages_with_cross_encoder page_docs argument will be provided along with chunk docs (docs).")
        # First retrieve similar chunks by regular kb search
        similar_chunk_docs = self.search(q=q, k=cross_encoder_input_k) # each doc is typically a chunk.
        # Now pass them to cross_encoder for finer similarity analysis. It will compare question to similar doc contents:
        scores = self.cross_encoder.predict([[q, chunk_doc.page_content] for chunk_doc in similar_chunk_docs], activation_fct=torch.nn.Sigmoid(), apply_softmax=True)

        # Now only top k most related docs will be selected
        sorted_indices = np.argsort(-scores) # sort in a decreasing score order.
        page_docs_indexes: Dict[int, Tuple[float, float]] = {} # stores the doc indexes of most similar docs. doc_index: (dist_score, cross_encoder_score)
        for i in sorted_indices:
            doc = similar_chunk_docs[i]
            if doc.metadata.get('doc_index') is None: raise AttributeError('search_pages_with_cross_encoder methods needs doc_index attribute for the docs in order to perform!')
            page_docs_indexes[doc.metadata["doc_index"]] = scores[i], doc.metadata["retrieval_info"]["dist"]
            if len(page_docs_indexes) >= max_k: break

        # Now extract and deep copy those most similar page-docs to thread-safely modify them:
        related_page_docs = []
        for doc_index, scores in page_docs_indexes.items():
            page_doc = self.page_docs[doc_index].copy(deep=True)
            page_doc.metadata["retrieval_info"] = {"q": q, "dist": scores[1], "cross_encoder_score":scores[0]} # I kept the key as dist even though it is not exactly a distance measure just too keep it compatible.
            related_page_docs.append(page_doc)

        return related_page_docs

