from typing import Any, Dict, Protocol, Union, List
from torch import Tensor
from numpy import ndarray

class Doc(Protocol):
    page_content: str
    metadata: Dict[str, Any]



class DB(Protocol):
    def similarity_search(self, sentences:Union[str, List[str]]) -> Union[List[Tensor], ndarray, Tensor]:
        ...



from langchain.embeddings.openai import OpenAIEmbeddings

