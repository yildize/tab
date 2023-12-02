from utils.doc_splitter import DocSplitter

ds = DocSplitter(docs_path="./storage/docs/summarized_docs.pkl")
ds.split(save_split_docs=True)