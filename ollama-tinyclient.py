import requests

def ask_question(content: str):
    response = requests.get("http://0.0.0.0:8001/ask", params={"content": content})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get response from server"}

if __name__ == "__main__":
    question = "What is the capital of France?"
    response = ask_question(question)
    print(response)