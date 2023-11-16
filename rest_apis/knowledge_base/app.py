from flask import Flask, jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError
from rest_apis.knowledge_base.schemas import kb_query_schema, KBQuery, doc_schema
from knowledge_base.default_kb import DefaultKnowledgeBase
from splitters.pdf_splitter import PdfSplitter

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


pdf_splitter = PdfSplitter(local_src_path="./storage/sources")
splits = pdf_splitter.split()
kb = DefaultKnowledgeBase(docs=splits, embedder_name="all-mpnet-base-v2")


@app.route('/')
def index():
    return {"message": "/search endpoint expects a query {content:str, k?:int}"}


@app.route('/search', methods=['POST'])
def search():
    print(kb_query_schema.load(request.get_json()))
    query = KBQuery(**kb_query_schema.load(request.get_json()))
    docs = kb.search(q=query.content, k=query.k) if query.k else kb.search(q=query.content)
    docs_dumped = [doc_schema.dumps(doc) for doc in docs]
    return jsonify({"docs": docs_dumped})


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error": err.messages}), 400


if __name__ == '__main__':
    app.run(debug=True)