import json
import os.path

from utils.utils import ROOT_PATH

class QASConverter:
    """ For now this class is converting new formatted qas
    into old format to provide compatability with the UI."""

    def __init__(self, input_file_path:str):
        self._input_file_path = os.path.join(ROOT_PATH, input_file_path)
        self._input_list = self.__load_json()

    def convert(self):
        output_list = []

        for item in self._input_list:
            new_metadata = {}
            sources = []
            for md in item['metadata']:
                sources.append(f"{os.path.basename(md['source'])} [Page {md['page']}]")
            new_metadata['source'] = ', '.join(sources)
            new_metadata['page'] = -1

            new_item = item.copy()
            new_item['metadata'] = new_metadata
            output_list.append(new_item)

        self.__save_json(output_list=output_list)

    def __load_json(self):
        # Read the original JSON file
        with open(self._input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def __save_json(self, output_list):
        directory, file_name = os.path.split(self._input_file_path)
        name, extension = os.path.splitext(file_name)
        new_name = f"{name}_converted{extension}"
        output_file_path = os.path.join(directory, new_name)
        # Write the transformed data to a new JSON file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(output_list, file, ensure_ascii=False, indent=4)

        print(f"Converted qas saved as {output_file_path}")


if __name__ == "__main__":
    qasc = QASConverter(input_file_path="./storage/extracted_questions/qas_index_425_to_550_2023-12-02_16-18-19.json")
    qasc.convert()