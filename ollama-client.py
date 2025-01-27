import requests

url = "http://localhost:11434/api/chat"
data = {
    "model": "deepseek-r1:32b",
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)
print(response.json()['message']['content'])
