from flask import Flask, jsonify

from knowledge_base.default_kb import DefaultKnowledgeBase
from splitters.pdf_splitter import PdfSplitter

app = Flask(__name__)






pdf_splitter = PdfSplitter(local_src_path="./storage/sources")
splits = pdf_splitter.split()
kb = DefaultKnowledgeBase(docs=splits, embedder_name="all-mpnet-base-v2")
@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)