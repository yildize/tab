from rag.rag import DefaultRetrievalAugmentedGenerator
from splitters.pdf_splitter import PdfSplitter
import time

pdf_splitter = PdfSplitter(chunk_size=750, chunk_overlap=0, local_src_path="./storage/sources/uni")
splits = pdf_splitter.split()

test_rag = DefaultRetrievalAugmentedGenerator(docs=splits)
while True:
    q = input("Enter your question:")
    st = time.time()
    answer = test_rag.ask(question=q)
    print(answer)
    et = time.time()
    print(f"-------- {et-st:.2f} seconds ----------")