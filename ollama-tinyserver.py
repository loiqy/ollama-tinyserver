import asyncio
from ollama import AsyncClient
import nest_asyncio
from fastapi import FastAPI
import uvicorn

nest_asyncio.apply()

client = AsyncClient(
    host='http://localhost:8000',
)
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/ask")
async def ask_question(content: str):
    message = {'role': 'user', 'content': content}
    response = await client.chat(model='deepseek-r1:32b', messages=[message])
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)