from langchain.embeddings import HuggingFaceEmbeddings

from splitters.pdf_splitter import PdfSplitter
from sentence_transformers import SentenceTransformer
from knowledge_base.chroma_kb import ChromaKB

hf = HuggingFaceEmbeddings(
    model_name='sentence-transformers/msmarco-MiniLM-L-6-v3',
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)


kb = ChromaKB(embedder=hf, docs_path="./storage/splits/docs")
pdf_splitter = PdfSplitter(local_src_path="./storage/sources")
splits = pdf_splitter.split(save=True)
