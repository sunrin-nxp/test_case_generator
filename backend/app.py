from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from test_case_generator import generate_test_cases
from bson.json_util import dumps
import os

CLIENT = os.getenv("CLIENT")

app = Flask(__name__)
app.config["MONGO_URI"] = CLIENT
mongo = PyMongo(app)

@app.route('/generate-testcases', methods=['POST'])
def generate_testcases():
    data = request.get_json()
    language = data.get('language')
    problem = data.get('problem')
    input_values = data.get('inputValues')
    output_values = data.get('outputValues')

    test_cases = generate_test_cases(language, problem, input_values, output_values)

    # 데이터베이스에 저장
    mongo.db.testcases.insert_one({
        'language': language,
        'problem': problem,
        'input_values': input_values,
        'output_values': output_values,
        'test_cases': test_cases
    })

    return jsonify({'testCases': test_cases})

@app.route('/testcases', methods=['GET'])
def get_testcases():
    testcases = mongo.db.testcases.find()
    return dumps(testcases)

if __name__ == '__main__':
    app.run(debug=True)