import aiohttp
import asyncio
from typing import TypedDict, List, Any, TypeAlias
from typing_extensions import NotRequired
import requests

class LLM_input(TypedDict):
    system_prompt: NotRequired[str]
    image: NotRequired[List[Any]]
    history: NotRequired[List[Any]]
    query : str

LLM_output : TypeAlias = str
    
class LLM():
    def __init__(self,
                 model_name : str,
                 api_keys : str|None,) -> None:
        
        self.model_name = model_name
        self.api_keys = api_keys

    def predict(self, input: LLM_input) -> LLM_output:
        
        response = self.API_server(input)
        
        return response

    async def predict_async(self, input: LLM_input) -> LLM_output:
        
        response = await self.API_server_async(input)
        
        return response

class OLLAMA(LLM):
    def __init__(self, 
                 model_name: str,
                 api_keys : str|None,   # 实际上是url
                 ) -> None:
        
        super().__init__(model_name, api_keys)

    def API_server(self, input: LLM_input) -> LLM_output:
        messages = self.messages(input)
        
        if input.get('response_format'):
            raise ValueError("response_format is not supported in this model")
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }

        response = requests.post(self.api_keys, json=data)
        return response.json()['message']['content']

    async def API_server_async(self, input: LLM_input) -> LLM_output:
        messages = self.messages(input)

        if input.get('response_format'):
            raise ValueError("response_format is not supported in this model")
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_keys, json=data) as response:
                content = await response.json()
                return content['message']['content']

    def messages(self, input: LLM_input) -> List[dict]:
        
        messages = []
        if input.get("system_prompt"):
            messages.append({
                "role": "system",
                "content": input["system_prompt"]
            })
        messages.append({
            "role": "user",
            "content": input["query"]
        })
        # content =[{"type": "text", "text": input["query"]}]
        
        if input.get('image'): #image should be a list of base64 encoded images
            raise ValueError("image is not supported in this model")
            image_file = [image for image in input.get('image')]
            for image in image_file:
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                            }
                        }
                    )
        # messages.append({"role": "user", "content": content})
        
        return messages
    
if __name__ == "__main__":
    model_name = "deepseek-r1:32b"
    api_keys = "http://localhost:11434/api/chat"
    ollama = OLLAMA(model_name, api_keys)

    # Test sync
    input = {
        "query": "What is the capital of France?"
    }
    response = ollama.predict(input)
    print(response)

    # Test async
    inputs = [
        {
            "query": "What is the capital of France?"
        },
        {
            "query": "What is the capital of Spain?"
        },
        {
            "query": "What is the capital of Italy?"
        }
    ]
    async def process_batch(batch):
        tasks = [ollama.predict_async(i) for i in batch]
        return await asyncio.gather(*tasks)
    responses = asyncio.run(process_batch(inputs))
    for response in responses:
        print(response)