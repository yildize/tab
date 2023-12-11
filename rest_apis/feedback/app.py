from flask import Flask, jsonify, request
from flask_cors import CORS
from marshmallow import ValidationError

from rest_apis.feedback.arg_parser import parser
from rest_apis.feedback.db_handler import DBHandler
from rest_apis.feedback.schemas import answer_feedback_schema, AnswerFeedback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/feedback', methods=['POST'])
def ask():
    #request_data = json.loads(request.data.decode('utf-8'))
    request_data = request.get_json()
    answer_feedback = AnswerFeedback(**answer_feedback_schema.load(request_data))
    db_handler.insert_feedback(is_rag=answer_feedback.is_rag, is_liked=answer_feedback.is_liked, user_question=answer_feedback.user_question,
                               matched_question=answer_feedback.matched_question, matched_answer=answer_feedback.matched_answer,
                               suggested_answer=answer_feedback.suggested_answer, rag_answer=answer_feedback.rag_answer, sources=answer_feedback.sources)
    return jsonify({"storage_successful":True})

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"error": err.messages}), 400

if __name__ == '__main__':
    # To run from terminal, position to the project root and then: python -m rest_apis.knowledge_base.app -- args
    args = parser.parse_args()

    db_handler = DBHandler()

    if args.serve_style == "waitress":
        from waitress import serve
        print(f"Serving through waitress on {args.host}:{args.port} with {args.num_threads} worker threads.")
        serve(app, host=args.host, port=args.port, threads=args.num_threads)

    else:
        app.run(host=args.host, port=args.port, debug=False)
