from knowledge_base.default_kb import DefaultKnowledgeBase
from knowledge_base.lc_kb import LangchainKnowledgeBase
from splitters.pdf_splitter import PdfSplitter
from utils.enums import LCVectorStores

pdf_splitter = PdfSplitter(local_src_path="./storage/sources/antalya-guide.pdf")
splits = pdf_splitter.split(save=False)

from langchain.embeddings import HuggingFaceEmbeddings



#kb = LangchainKnowledgeBase(docs=splits, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"), type=LCVectorStores.FAISS)
#res = kb.search(query="Where is the ucansu waterfall?", scores=True)


kb = DefaultKnowledgeBase(docs=splits, embedder_name="all-mpnet-base-v2")
res = kb.search(q="kaleiçi")


# for elm in res:
#     print(elm.page_content)
#     print(elm.metadata)
#     print("#######################")

for elm in res:
    print(elm.page_content)
    print(elm.metadata)
    print("---------------")