import os
from utils.utils import ROOT_PATH


class Path:
    """
    A utility class to help handle source file paths.
    """

    def __init__(self, path_list:list[str] | str):
        if isinstance(path_list, str):
            path_list = [path_list]
        if not isinstance(path_list, list):
            ValueError("Expected a list of strings as the 'paths'!")
        self.path_list = self.__convert_paths_to_abs(path_list)

        if not self.__paths_valid():
            FileNotFoundError(f"Some of the paths are not found for the list {self.path_list}. "
                              f"You should either provide absolute paths or provide paths relative to {ROOT_PATH}")

        self.path_list = self.__get_all_files()

    def __convert_paths_to_abs(self, path_list:list[str]):
        return [os.path.abspath(os.path.join(ROOT_PATH, path)) if not os.path.isabs(path) else path for path in path_list]

    def __paths_valid(self) -> bool:
        return all([os.path.exists(path=path) for path in self.path_list])

    def __get_all_files(self):
        """Given a list of paths, retrieve all files within those directories (recursively)."""
        all_files = []

        for path in self.path_list:
            # If it's a file, simply append to the list
            if os.path.isfile(path):
                all_files.append(path)

            # If it's a directory, walk through it to get all files
            elif os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        all_files.append(os.path.join(dirpath, filename))

        return all_files

    def __extract_files_from_dirs(self):
        for path in self.path_list:
            # Check if it is a directory
            if os.path.isdir(path):
                all_items = os.listdir(path)
                files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

            # remove folders add files instead





