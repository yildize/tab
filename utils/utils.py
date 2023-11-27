import os
import pickle
from typing import Dict, Any, Union
import json
from utils.protocols import Doc
from dataclasses import dataclass
from typing import List


def root_path():
    project_name = "tab"
    # Start with the directory of the current module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up the directories until we reach the 'tab' directory
    # (You might need to adjust this logic based on your exact project structure.)
    while os.path.basename(current_dir) != project_name:
        current_dir = os.path.dirname(current_dir)
    return current_dir


ROOT_PATH = root_path()


def load_docs(docs_path: str):
    """ This function is used to load a pickle object."""
    if not os.path.isabs(docs_path): docs_path = os.path.join(ROOT_PATH, docs_path)
    with open(docs_path, 'rb') as file:
        return pickle.load(file)


def load_qa_pairs_json_as_docs(qa_pairs_json_path: str) -> List[Doc]:
    """ This function is used to load question-answer pair json file as a List[Doc] by embedding answer into metadata."""
    if not os.path.isabs(qa_pairs_json_path): qa_pairs_json_path = os.path.join(ROOT_PATH, qa_pairs_json_path)
    with open(qa_pairs_json_path, 'r') as json_file:
        qa_list: List[Dict[str, Any]] = json.load(json_file)
    docs = []
    for qa_dict in qa_list:
        page_content = qa_dict["question"]
        metadata = qa_dict["metadata"]
        # add answer inside the metadata to keep it as a doc
        metadata["answer"] = qa_dict["answer"]
        docs.append(DummyDoc(page_content=page_content, metadata=metadata))
    return docs


def load_qa_pairs(qa_pairs_path:str)->List[Doc]:
    """ This function is used to load question-answer pair from both a json file or a pickle file."""
    if not os.path.isabs(qa_pairs_path): qa_pairs_path = os.path.join(ROOT_PATH, qa_pairs_path)
    _, file_extension = os.path.splitext(qa_pairs_path)
    if file_extension == ".json": return load_qa_pairs_json_as_docs(qa_pairs_path)
    return load_docs(qa_pairs_path)


class Question:
    def __init__(self, q: str, doc:Doc):
        self.question, self.doc = q, doc


class QAPair:
    def __init__(self, q: str, a: str, m: Union[dict[str, Any], List[dict[str, Any]]]):
        self.question, self.answer, self.metadata = q, a, m

    # This method will convert the object to a dictionary which can be serialized
    def to_dict(self) -> dict:
        return {
            'question': self.question,
            'answer': self.answer,
            'metadata': self.metadata
        }


class QAS:

    def __init__(self):
        self.storage: list[QAPair] = []

    def add_pair(self, qa_pair: QAPair):
        self.storage.append(qa_pair)

    def save_to_json(self, file_path: str):
        # Convert the list of QAPair objects to a list of dictionaries
        storage_as_dicts = [qa_pair.to_dict() for qa_pair in self.storage]
        # Serialize the list of dictionaries to JSON and write it to a file
        with open(file_path, 'w') as json_file:
            json.dump(storage_as_dicts, json_file, ensure_ascii=False, indent=4)

    def save_as_docs(self, file_path:str):
        # Convert the lis of QAPair objects to list of Docs:
        docs = []
        for qa_pair in self.storage:
            page_content = qa_pair.to_dict()["question"]
            metadata = qa_pair.to_dict()["metadata"]
            # add answer inside the metadata to keep it as a doc
            metadata["answer"] = qa_pair.to_dict()["answer"]
            docs.append(DummyDoc(page_content=page_content, metadata=metadata))
        with open(file_path, 'wb') as output:
            pickle.dump(docs, output, pickle.HIGHEST_PROTOCOL)


@dataclass
class DummyDoc:
    page_content:str
    metadata: dict