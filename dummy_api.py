from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return {"message": "Hey"}

@app.route('/api/question', methods=['POST'])
def search():
    #request_data = json.loads(request.data.decode('utf-8'))
    request_data = request.get_json() # "{'sender': 'dummy_sender_name', 'user_question': 'dasd', 'time_tag': '2023-12-08T16:31'}"

    request_data["answer"] = "Example matched answer."
    request_data["matched_question"] = "Example matched question"
    request_data["similarity"] = 0.7
    request_data["meta_data"] =  {"source_name":"example_source", "page":0}
    request_data["extra_questions"] =  {"questions":["extra q 1", "extra q 2"], "similarities":[0.6, 0.5]}

    return jsonify(request_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

