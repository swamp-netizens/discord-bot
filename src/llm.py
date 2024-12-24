import json
import logging

import aiohttp


AI_ENDPOINT = "http://192.168.0.192:5000/v1/completions"

logger = logging.getLogger("llm")

async def query_ai(prompt):
    """Query the AI endpoint with a prompt"""
    try:
        payload = {
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.6,
            "seed": 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(AI_ENDPOINT, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('text', 'No response from AI')
                else:
                    logger.error(f"AI API error: {response.status}")
                    return "Sorry, I couldn't get a response from the AI right now."
    except Exception as e:
        logger.error(f"Error querying AI: {e}")
        return "Sorry, there was an error communicating with the AI."



# mainly used for testing. Should not be used in production unless the user is aware that openai or anthropic or other apis are used
async def query_open_router(prompt: str) -> str:
    OPENROUTER_API_KEY="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"
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

class OpenRouterLlm():
    async def query_ai(self, prompt:str)-> str:
        return await query_open_router(prompt)

class LocalLlm:
    async def query_ai(self, prompt: str):
        return await query_ai(prompt)

