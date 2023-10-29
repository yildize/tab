import os
import pickle

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




