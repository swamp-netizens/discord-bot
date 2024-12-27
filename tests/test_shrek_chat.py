import pytest

from src.shrek_chat import create_shrek_chat, ChatMessage, ShrekChat


def test_get_completion():
    class MockDeps():
        async def query_ai(self, s: str) -> str:
            return "Cowabunga dude!"

    res =  create_shrek_chat()
    assert res[0].role == "system"
    assert res[0].message == "You are shrek. You must act like shrek. You can never break character."
    assert res[1].role == "assistant"
    assert res[1].message == "Och, fine, laddie, let's jist get this talk started already!"
