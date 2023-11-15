from abc import ABC, abstractmethod
from typing import Optional, List


class BaseEvaluator(ABC):

    def __init__(self):
        self.ground_truth_answers: Optional[List[str]] = None
        self.system_answers: Optional[List[str]] = None

    def evaluate(self, ground_truth_answers:List[str], system_answers:List[str]) -> float:
        """ This method will compare the ground truth answers with the system answers and return and evaluation score"""
        self.ground_truth_answers = ground_truth_answers
        self.system_answers = system_answers
        self.__check_validity()
        return self._evaluation_logic()


    @abstractmethod
    def _evaluation_logic(self) -> float:
        """ This method will be overriden, by the children to implement the specialized evaluation logic"""
        ...

    def __check_validity(self):
        if len(self.ground_truth_answers) != len(self.system_answers):
            raise ValueError(f"Num ground truth answers ({len(self.ground_truth_answers)}) should be equal"
                             f"to the num predicted system answers ({len(self.system_answers)}) for the evaluation.")