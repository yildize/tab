import langchain.schema.document
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from utils.path import Path
from utils.protocols import Doc
from splitters.base_local_splitter import LocalSplitter


class PdfSplitter(LocalSplitter):

    def __init__(self, local_src_path:List[str]|str|Path, chunk_size:int=1000, chunk_overlap:int=0):
        super().__init__(local_src_path=local_src_path)
        self.__text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function = len)

    def _load_logic(self, abs_paths: List[str]) -> List[Doc]:
        """ Will load the source pdf paths as list of page docs"""
        docs = []
        for path in abs_paths:
            page_docs = PyPDFLoader(path).load()
            docs.extend(page_docs)
        return docs  # will contain all source's all pages. Each page as a doc.

    def _split_logic(self, docs: List[Doc]) -> List[Doc]:
        """ Will convert list of page docs into list of chunk docs"""
        # Each page doc will be splitted separately. So we'll obtain multiple chunk docs from each page doc:
        if not isinstance(docs[0], langchain.schema.document.Document):
            ValueError(f"Since you use a built-in splitter it expects List of Documents but you provided List of{type(docs[0])}")

        chunk_docs = self.__text_splitter.split_documents(docs)
        return chunk_docs





