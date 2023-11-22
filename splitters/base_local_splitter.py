import datetime
import os
import pickle
from abc import ABC, abstractmethod
from typing import List, Union

from utils.path import Path
from utils.protocols import Doc
from utils.utils import ROOT_PATH


class LocalSplitter(ABC):

    def __init__(self, local_src_path:Union[List[str], str, Path]):
        self.local_src_path = local_src_path
        # Convert a local path into a Path for utilities
        if not isinstance(self.local_src_path, Path): self.local_src_path = Path(self.local_src_path)

    def split(self, save:bool=False, load_only:bool=False, both_load_and_split:bool=False) -> Union[List[Doc]]:
        """
        Splits the documents at the given path into chunks.

        :param local_src_path: Path to the local documents to load and split.
        :return: List of docs each representing a chunk
        """
        # Load the docs and split them with provided logics:
        docs = self._load_logic(abs_paths=self.local_src_path.path_list)
        if load_only: doc_list = docs
        elif both_load_and_split: doc_list = (docs, self._split_logic(docs=docs))
        else: doc_list = self._split_logic(docs=docs)
        if save: self.__save_splits(doc_list)
        return doc_list


    @abstractmethod
    def _load_logic(self, abs_paths: List[str]) -> List[Doc]:
        """ Will load the provided list of paths into List of Docs. A return Doc can be a page or the whole source."""
        ...

    @abstractmethod
    def _split_logic(self, docs: List[Doc]) -> List[Doc]:
        """ Will convert list of source Docs into list of chunk docs!"""
        ...

    def __save_splits(self, splits:List[Doc]):
        formatted_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_path = os.path.join(ROOT_PATH, "storage", "splits", f"splits_{formatted_date}")
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path): os.makedirs(dir_path)
        with open(save_path, 'wb') as file:
            pickle.dump(splits, file)
        print(f"Splits saved to {save_path}")
