import json
from typing import List, Dict, Any
from collections import Counter
import os


class DummyQACleaner:
    """ This class is the most basic ruled based cleaner for the derived qa pairs. I am planning to provide
    a more capable cleaner or maybe a correcter utilizing an LLM. That is why I call this class as dummy."""
    def __init__(self, file_path:str, banned_phrases=("this document",)):
        self._file_path = file_path
        with open(file_path, 'r') as json_file:
            self._qa_list: List[Dict[str, Any]] = json.load(json_file)
        self._banned_phrases = banned_phrases

        self._counter = Counter(dict_elm["question"] for dict_elm in self._qa_list)

    def clean(self):
        cleaned_qa_list = []
        seen_questions = set()
        eliminated_due_to_banned_phrase, eliminated_due_to_duplication = 0,0
        for dict_elm in self._qa_list:
            question = dict_elm["question"]
            # For each dict element first check if it includes any banned phrases,  we won't be keeping it if it does.
            if self.__question_has_a_banned_phrase(question):
                eliminated_due_to_banned_phrase += 1
                continue
            # Now check if this question is seen so far, in that case we won't be keeping it.
            if question in seen_questions:
                eliminated_due_to_duplication += 1
                continue
            # If question is clean keep it and add question to the seen
            seen_questions.add(question)
            cleaned_qa_list.append(dict_elm)

        num_eliminated = eliminated_due_to_banned_phrase+eliminated_due_to_duplication
        num_left = len(self._qa_list) - num_eliminated
        print(f"In total of {num_eliminated}/{len(self._qa_list)} pairs are eliminated and left with {num_left} questions. {eliminated_due_to_banned_phrase} of them "
              f"due to usage of banned phrases {self._banned_phrases} and {eliminated_due_to_duplication} of them due to question duplication.")

        self.__save_cleaned_qas(cleaned_qa_list)

    def how_many_unique_questions(self):
        print(len(self._counter))

    def top_n_questions(self, n=5):
        # Order the Counter in decreasing order of counts
        ordered_counter = self._counter.most_common()
        for i, qc in enumerate(ordered_counter):
            print(qc)
            if i+1 == n:break

    def __question_has_a_banned_phrase(self, question:str):
        for banned_phrase in self._banned_phrases:
            if banned_phrase in question: return True
        return False

    def __save_cleaned_qas(self, cleaned_qas:List[Dict[str, Any]]):
        # Get the file name without the extension
        file_path_without_extension = os.path.splitext(self._file_path)[0]
        clean_file_path = file_path_without_extension+"_cleaned.json"
        # Open the output file in write mode
        with open(clean_file_path, 'w') as json_file:
            # Write the list of dictionaries as JSON to the file
            json.dump(cleaned_qas, json_file, indent=4)  # Use indent for pretty formatting
        print(f"Cleaned qas saved as {clean_file_path}")
