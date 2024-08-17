# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import subprocess

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['code_db']
collection = db['executions']

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data['code']
    range_values = data['range'].split(',')

    results = []
    for value in range_values:
        try:
            # subprocess를 사용하여 Python 코드 실행 (보안에 유의)
            formatted_code = code.replace("{value}", value)
            process = subprocess.run(
                ['python3', '-c', formatted_code],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = process.stdout
        except Exception as e:
            output = str(e)

        result = {
            'input': value,
            'output': output
        }
        results.append(result)
        collection.insert_one(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
