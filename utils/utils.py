import os


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




