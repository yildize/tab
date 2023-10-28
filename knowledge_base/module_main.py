import os
import pickle
from utils.utils import ROOT_PATH


with open(os.path.join(ROOT_PATH, "storage", "splits", "splits_2023-10-28_13-52-17"), 'rb') as file:
    loaded_documents = pickle.load(file)

loaded_documents


from sentence_transformers import SentenceTransformer

from langchain.embeddings import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embedder = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

ress = embedder.embed_documents()
