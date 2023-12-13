import os
from proxies.proxy_kb import ProxyKnowledgeBase
from proxies.proxy_mistral_llm import ProxyMistralLLM
from proxies.proxy_rag import ProxyRAG
from rag.rag import DefaultRetrievalAugmentedGenerator
from rag.rag_advanced import RAGAdvanced
from splitters.pdf_splitter import PdfSplitter
import time



# llm = ProxyMistralLLM(endpoint_url="http://3fe1-35-196-54-177.ngrok-free.app/ask")
# kb = ProxyKnowledgeBase(base_endpoint_url="127.0.0.1:5000")
# test_rag = RAGAdvanced(llm=llm, kb=kb)

test_rag = ProxyRAG(endpoint_url="127.0.0.1:5005/ask")
#answer, metadata = rag.ask(question="Give me a full list of Research Assistant names for Hacettepe University CS department.", k=7, cross_encoder_input_k=50)

from evaluation.evaluation_set import EvaluationSet
from evaluation.bleu_evaluator import BleuEvaluator
from evaluation.semantic_evaluator import SemanticEvaluator


evaluation_set = EvaluationSet()

from ctransformers import AutoModelForCausalLM

answers = []
answer_times = []
for qa in evaluation_set.qas:
    print(f"Question: '{qa.q}' ")
    st = time.time()
    answer, metadata = test_rag.ask(question=qa.q, k=5, cross_encoder_input_k=100)

    # Extract base names and pages, and combine them into a single string
    combined_source = ', '.join(
        f"{os.path.basename(d['source'])} [page {d['page']}]"
        for d in metadata
    )
    # Create the final dictionary
    metadata = {"source": combined_source, "page": -1}

    print("Anwer: ",answer)
    print("Metadata:", metadata)
    answers.append(answer)
    et = time.time()
    #print(f"RAG Answer: '{answer}'")
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

"""
Bleu Score: ([0.006518732539784603, 0.20838154762866123, 0.08046931098187607, 0.24065691382368773, 0.1008372348628028], 0.12737274796736248)
Semantics Score: (tensor([0.7584, 0.8810, 0.8811, 0.7684, 0.9099]), 0.8397736549377441)
Average Answering Time: 64.72351417541503


Bleu Score: ([0.008435193159550772, 0.20939723321538242, 0.39508656645560836, 0.08359621144959146, 0.06838548730382311], 0.15298013831679122)
Semantics Score: (tensor([0.8296, 0.8619, 0.8605, 0.6815, 0.9106]), 0.828809916973114)
Average Answering Time: 64.89236621856689
"""