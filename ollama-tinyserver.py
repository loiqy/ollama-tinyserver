import asyncio
from ollama import AsyncClient
import nest_asyncio

nest_asyncio.apply()

client = AsyncClient()

async def chat():
    message = {'role': 'user', 'content': '为什么天空是蓝色的？'}
    response = await client.chat(model='deepseek-r1:32b', messages=[message])
    print(response)

asyncio.run(chat())

