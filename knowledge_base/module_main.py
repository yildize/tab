from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer


kb = ChromaKB(embedder=hf, docs_path="./storage/splits/docs")
kb