import torch

from evaluation.base_evaluator import BaseEvaluator
from sentence_transformers import util

from knowledge_base.embedders import SetenceTransformerEmbedder
import warnings


class SemanticEvaluator(BaseEvaluator):
    """ This is a semantic evaluator which utilizes sentence-transformers to compare meanings in embedding space"""

    def __init__(self, check_longs=True):
        super().__init__()
        self.embedder = SetenceTransformerEmbedder(embedder_name='all-mpnet-base-v2')
        self._check_longs = check_longs

    def _evaluation_logic(self) -> float:
        """ This method will compare the ground truth answers with the system answers and return and evaluation score"""
        if self._check_longs: self._check_for_long_sentences()
        # Let's obtain the embedding representations for the provided answers utilizing setence-transformer.
        gt_embds, sys_embds = self.embedder(self.ground_truth_answers), self.embedder(self.system_answers)
        full_cosine_scores = util.cos_sim(gt_embds, sys_embds) # nxn matrix representing similarity between each elm.
        scores = torch.diag(full_cosine_scores) #todo:  Handling negative similarities, although it is rare.
        # Although it is rare for sentence-embedders to have negative similarities, I will be clamping the results just to be safe
        clamped_scores = torch.clamp(scores, min=0, max=1)
        return clamped_scores.mean().item()

    def _check_for_long_sentences(self):
        num_pairs = len(self.ground_truth_answers )
        for i,sentence in enumerate(self.ground_truth_answers + self.system_answers):
            if self.embedder.text_exceeds_max_seq_len(text=sentence): ...
                # long_sentence_descriptor = f"Index {i} of Sentence of Ground Truths" if i < num_pairs else f"Index {i-num_pairs} of Sentence of System Answers"
                # #warnings.warn(f"{long_sentence_descriptor} is too long ({self.embedder.len_required_tokens(sentence)} tokens needed) "
                # #              f"to embed  with this embedder model (max {self.embedder.max_seq_length} tokens)")


