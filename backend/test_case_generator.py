import requests

def generate_test_cases(language, problem, input_values, output_values):
    
    test_cases = []
    for input_val, output_val in zip(input_values, output_values):
        test_cases.append({'input': input_val.strip(), 'output': output_val.strip()})
    return test_cases

def query_chatgpt(prompt, api_key):
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


api_key = ''
prompt = "안녕하세용"

try:
    response = query_chatgpt(prompt, api_key)
    print("")
    print(response)
except Exception as e:
    print(f"Error: {e}")