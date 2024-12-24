import pytest
from src.shrek_chat import create_shrek_chat, LlmInterface
import json
import aiohttp


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




@pytest.mark.skip
@pytest.mark.asyncio
async def test_open_router_mock():
    res = await query_open_router("what is love?")
    print(res)
    assert len(res) > 0

@pytest.mark.skip
@pytest.mark.asyncio
async def test_full_chat():
    class MockDeps(LlmInterface):
        async def query_ai(self, s: str) -> str:
            return await query_open_router(s)

    dps: LlmInterface = MockDeps()
    res = await create_shrek_chat(dps, "what is love?")
    print(res[2].message)
    print(res)



@pytest.mark.asyncio
async def test_get_completion():
    class MockDeps(LlmInterface):
        async def query_ai(self, s: str) -> str:
            return "Cowabunga dude!"

    dps: LlmInterface = MockDeps()
    res = await create_shrek_chat(dps, "what is love?")
    assert res[0].role == "system"
    assert res[0].message == "You are shrek. You must act like shrek. You can never break character."
    assert res[1].role == "user"
    assert res[1].message == "what is love?"
    assert res[2].role == "assistant"
    assert res[2].message == "Cowabunga dude!"
    print(res)
