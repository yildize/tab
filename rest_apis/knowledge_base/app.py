from flask import Flask, jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError
from sentence_transformers import SentenceTransformer

from rest_apis.knowledge_base.schemas import kb_query_schema, KBQuery, doc_schema
from knowledge_base.default_kb import DefaultKnowledgeBase
from splitters.pdf_splitter import PdfSplitter
from rest_apis.knowledge_base.arg_parser import parser
from utils.utils import load_qa_pairs, load_docs

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return {"message": "/search endpoint expects a query {content:str, k?:int}"}


@app.route('/search', methods=['POST'])
def search():
    query = KBQuery(**kb_query_schema.load(request.get_json()))
    docs = kb.search(q=query.content, k=query.k) if query.k else kb.search(q=query.content)
    docs_dumped = [doc_schema.dump(doc) for doc in docs]
    return jsonify({"docs": docs_dumped})


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error": err.messages}), 400


if __name__ == '__main__':
    # To run from terminal, position to the project root and then: python -m rest_apis.knowledge_base.app -- args
    args = parser.parse_args()

    if args.source_type == 'pdfs':
        pdf_splitter = PdfSplitter(local_src_path=args.source_path, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
        docs = pdf_splitter.split()
    elif args.source_type == 'qa_docs':  # this should work for qa_json as well
        docs = load_qa_pairs(qa_pairs_path=args.source_path)
    else:  # "docs"
        docs = load_docs(docs_path=args.source_path)

    kb = DefaultKnowledgeBase(docs=docs, embedder_name=args.embedder_name) # use lock for thread safety

    if args.serve_style == "waitress":
        from waitress import serve
        print(f"Serving through waitress on {args.host}:{args.port} with {args.num_threads} worker threads.")
        serve(app, host=args.host, port=args.port, threads=args.num_threads)

    else:
        app.run(host=args.host, port=args.port, debug=True)

