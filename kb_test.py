from knowledge_base.default_kb import DefaultKnowledgeBase
from utils.utils import load_docs

docs =  load_docs(docs_path="./storage/docs/summarized_docs_split.pkl")
#page_docs = load_docs(docs_path="./storage/docs/summarized_docs.pkl")

kb = DefaultKnowledgeBase(docs=docs, embedder_name="all-mpnet-base-v2", cross_encoder_name="cross-encoder/ms-marco-MiniLM-L-6-v2", page_docs="./storage/docs/summarized_docs.pkl")
kb.search_pages_with_cross_encoder(q="cemil")