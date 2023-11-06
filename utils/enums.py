import enum

class LCVectorStores(enum.IntEnum):
    Chroma = 0
    FAISS = 1
    SVM_Retriever = 2

class MistralTypes(enum.IntEnum):
    GPTQ_4bit = 0
    GPTQ_8bit = 1
    GGUF_Q5 = 2
    GGUF_Q6 = 3