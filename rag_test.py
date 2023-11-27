from rag.rag import DefaultRetrievalAugmentedGenerator
from splitters.pdf_splitter import PdfSplitter
import time

pdf_splitter = PdfSplitter(chunk_size=1000, chunk_overlap=0, local_src_path="./storage/sources/uni")
splits = pdf_splitter.split()

test_rag = DefaultRetrievalAugmentedGenerator(docs=splits)
from evaluation.evaluation_set import EvaluationSet
from evaluation.bleu_evaluator import BleuEvaluator
from evaluation.semantic_evaluator import SemanticEvaluator


evaluation_set = EvaluationSet()


answers = []
answer_times = []
for qa in evaluation_set.qas:
    print(f"Question to be asked: '{qa.q}' ")
    st = time.time()
    answer = test_rag.ask(question=qa.q)
    answers.append(answer)
    et = time.time()
    print(f"RAG Answer: '{answer}'")
    answer_time = et-st
    answer_times.append(answer_time)
    print(f"-------- {answer_time:.2f} seconds ----------")


# Evaluation
be = BleuEvaluator()
se = SemanticEvaluator()

print("Bleu Score:", be.evaluate(ground_truth_answers=evaluation_set.answers, system_answers=answers))
print("Semantics Score:", se.evaluate(ground_truth_answers=evaluation_set.answers, system_answers=answers))
print("Average Answering Time:", sum(answer_times)/len(answer_times))

# while True:
#     q = input("Enter your question:")
#     st = time.time()
#     answer = test_rag.ask(question=q)
#     print(answer)
#     et = time.time()
#     print(f"-------- {et-st:.2f} seconds ----------")