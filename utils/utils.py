import os
import pickle
from typing import Dict, Any
import json
from utils.protocols import Doc


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
    if not os.path.isabs(docs_path): docs_path = os.path.join(ROOT_PATH, docs_path)
    with open(docs_path, 'rb') as file:
        return pickle.load(file)


class Question:
    def __init__(self, q: str, doc:Doc):
        self.question, self.doc = q, doc

class QAPair:
    def __init__(self, q: str, a: str, m: dict[str, Any]):
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
