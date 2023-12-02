import os
from typing import List, Tuple, Dict, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.utils import load_docs, save_docs

from datetime import datetime

class DocSplitter:
    """This is a utility class to convert docs into split docs."""
    def __init__(self, docs_path:str, split_info:Tuple[Tuple[int, int],...] = ((1000, 0), (500, 100), (250, 50), (100, 0), (25, 0))):
        """
        docs can be a path to docs or actual list of docs
        split_info is a tuple of tuples each inner tuple representing chunk_size and chunk_overlap arguments respectively.
        """
        self.docs_path = docs_path
        self.docs = load_docs(docs_path=docs_path)
        self.splitters = [RecursiveCharacterTextSplitter(chunk_size=info[0], chunk_overlap=info[1]) for info in split_info]

    def split(self, save_split_docs=True):
        chunk_docs = [chunk_doc for splitter in self.splitters for chunk_doc in splitter.split_documents(self.docs)]
        if save_split_docs:
            directory, filename = os.path.split(self.docs_path)
            base_name, extension = os.path.splitext(filename)
            modified_name = f"{base_name}_split_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}{extension}"
            save_docs(docs=chunk_docs, docs_path=os.path.join(directory, modified_name))
            print(f"Split docs successfully saved to:{os.path.join(directory, modified_name)}")


