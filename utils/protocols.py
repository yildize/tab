from typing import Any, Dict, Protocol, Union, List
from torch import Tensor
from numpy import ndarray

class Doc(Protocol):
    page_content: str
    metadata: Dict[str, Any]


class Embedder(Protocol):
    def encode(self, sentences:Union[str, List[str]]) -> Union[List[Tensor], ndarray, Tensor]: