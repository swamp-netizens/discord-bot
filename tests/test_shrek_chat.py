from src.shrek_chat import ChatMessage, create_shrek_chat, Dependencies


async def test_get_completion():
    class MockDeps(Dependencies):
        async def query_ai(self, s: str) -> str:
            return "Cowabunga dude!" + s

    message = ChatMessage("user", "what is love?")
    dps: Dependencies = MockDeps()
    res = await create_shrek_chat(dps, "what is love?")
    print(res)
