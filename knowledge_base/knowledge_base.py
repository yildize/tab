
from abc import ABC, abstractmethod

from sentence_transformers import CrossEncoder

from knowledge_base.embedders import Embedder
from typing import Union, List
from utils.protocols import Doc
from utils.utils import load_docs
from typing import Optional
import os
from utils.utils import ROOT_PATH

class CustomKnowledgeBase(ABC):

    def __init__(self, docs:Union[str, List[Doc]], embedder:Embedder, cross_encoder_name: Optional[str], page_docs:Optional[Union[str, List[Doc]]]):
        # If a path is specified as docs let's load it:
        self.docs = load_docs(docs) if isinstance(docs, str) else docs
        self.page_docs = load_docs(page_docs) if isinstance(page_docs, str) else page_docs
        self.embedder = embedder
        if cross_encoder_name is not None:
            cache_dir = os.path.join(ROOT_PATH, "storage", "cross-encoders")
            self._cross_encoder = CrossEncoder(model_name=cross_encoder_name, tokenizer_args={'cache_dir': cache_dir}, automodel_args={'cache_dir': cache_dir},  max_length=512)
            # In addition to cross_encoder I will be further splitting the incoming page_docs

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


    @property
    def cross_encoder_exists(self):
        return hasattr(self, "_cross_encoder")
    @property
    def cross_encoder(self):
        if self.cross_encoder_exists: return self._cross_encoder
        raise AttributeError("You are trying to reach the cross_encoder attribute of the knowledge base but you haven't"
                             "provided a cross_encoder_name to constructor.")


