import requests

url = "http://localhost:11434/api/generate"
data = {
    "model": "deepseek-r1:32b",
    "prompt": "Why is the sky blue?"
}

response = requests.post(url, json=data, stream=True)
full_response = ""

for line in response.iter_lines():
    if line:
        decoded_line = line.decode("utf-8")
        full_response += decoded_line + "\n"

print(full_response)