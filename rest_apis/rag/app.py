from flask import Flask, jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError

from proxies.proxy_kb import ProxyKnowledgeBase
from proxies.proxy_mistral_llm import ProxyMistralLLM
from rag.rag_advanced import RAGAdvanced
from rest_apis.rag.arg_parser import parser
from rest_apis.rag.schemas import doc_schema, rag_query_schema, RAGQuery
from utils.utils import load_docs
import inspect
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return {"message": "RAG endpoint expects /ask"}

@app.route('/ask', methods=['POST'])
def ask():
    #request_data = json.loads(request.data.decode('utf-8'))
    request_data = request.get_json()
    query = RAGQuery(**rag_query_schema.load(request_data))
    if args.rag_type == "search_pages": query.k = max(1, min(query.k, 10)) # for search pages limit k between 1-7 in order to not exceed the context size
    answer, metadata = rag.ask(question=query.question, k=query.k, cross_encoder_input_k=query.cross_encoder_input_k)
    return jsonify({"answer": answer, "metadata": metadata})

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error": err.messages}), 400


if __name__ == '__main__':
    # To run from terminal, position to the project root and then: python -m rest_apis.knowledge_base.app -- args
    args = parser.parse_args()

    args.llm_endpoint_url = "http://b837-35-231-87-216.ngrok-free.app/ask"
    args.base_kb_endpoint_url = "127.0.0.1:5001"

    rag = RAGAdvanced(llm=ProxyMistralLLM(endpoint_url=args.llm_endpoint_url), kb=ProxyKnowledgeBase(base_endpoint_url=args.base_kb_endpoint_url), search_pages=args.rag_type=="search_pages")

    if args.serve_style == "waitress":
        from waitress import serve
        print(f"Serving through waitress on {args.host}:{args.port} with {args.num_threads} worker threads.")
        serve(app, host=args.host, port=args.port, threads=args.num_threads)

    else:
        app.run(host=args.host, port=args.port, debug=True)

