import enum

class LCVectorStores(enum.IntEnum):
    Chroma = 0
    FAISS = 1
    SVM_Retriever = 2