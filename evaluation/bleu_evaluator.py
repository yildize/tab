import nltk
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction
from evaluation.base_evaluator import BaseEvaluator
from sentence_transformers import util
from nltk.tokenize import word_tokenize

from knowledge_base.embedders import SetenceTransformerEmbedder


class BleuEvaluator(BaseEvaluator):
    """ This is a semantic evaluator which utilizes sentence-transformers to compare meanings in embedding space"""

    def __init__(self):
        super().__init__()
        self.smoothing_func = SmoothingFunction()
        nltk.download('punkt')


    def _evaluation_logic(self) -> float:
        """ This method will compare the ground truth answers with the system answers and return and evaluation score.
        Formula: BP*exp(sum(w*log(p))) without smoothining."""
        scores = []
        # Calculate and print BLEU scores for each answer
        for system, truth in zip(self.system_answers, self.ground_truth_answers):
            # Tokenize the sentences into words
            truth_tokens = [nltk.word_tokenize(truth)]
            system_tokens = nltk.word_tokenize(system)

            # Calculate the BLEU score
            score = sentence_bleu(truth_tokens, system_tokens, smoothing_function=self.smoothing_func.method1)
            scores.append(score)

        return scores, sum(scores)/len(scores)


