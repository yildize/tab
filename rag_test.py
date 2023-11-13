from rag.rag import DefaultRetrievalAugmentedGenerator
from splitters.pdf_splitter import PdfSplitter

pdf_splitter = PdfSplitter(local_src_path="./storage/sources/tsps")
splits = pdf_splitter.split()

test_rag = DefaultRetrievalAugmentedGenerator(docs=splits)
while True:
    q = input("Enter your question:")
    answer = test_rag.ask(question=q)
    print(answer)
    print("--------------------------")