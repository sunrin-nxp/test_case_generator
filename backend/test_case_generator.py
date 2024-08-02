import requests
import openai
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from test_case_generator import generate_test_cases
from bson.json_util import dumps
import os

TOKEN = os.getenv("TOKEN")
CLIENT = os.getenv("CLIENT")

app = Flask(__name__)
app.config["MONGO_URI"] = CLIENT
mongo = PyMongo(app)

def generate_test_cases(language, problem, input_values, output_values):
    
    test_cases = []
    try:
        response = query_chatgpt()
        print("")
        test_cases = response.split("\n")
    except Exception as e:
        print(f"Error: {e}")
    return test_cases

def query_chatgpt(language, problem, input_values, output_values):
    api_key = TOKEN
    endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['text'].strip()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Error occurred: {err}")

    prompt = f"Generate test cases for the following problem: \n\nLanguage: {language}\nProblem: {problem}\nInput values: {input_values}\nOutput values: {output_values}\n\nTest cases:"
