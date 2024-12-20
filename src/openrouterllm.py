import aiohttp
import json

from shrek_chat import LlmInterface


# mainly used for testing. Should not be used in production unless the user is aware that openai or anthropic or other apis are used
async def query_open_router(prompt: str) -> str:
    OPENROUTER_API_KEY=""
    async with aiohttp.ClientSession() as session:
        async with session.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",

        },
        data=json.dumps({
            "model": "meta-llama/llama-3.1-8b-instruct",  # Optional
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })) as response:
            data = await response.json()
            return data['choices'][0]['message']['content']

class OpenRouterLlm(LlmInterface):
    async def query_ai(self, prompt:str)-> str:
        return await query_open_router(prompt)


