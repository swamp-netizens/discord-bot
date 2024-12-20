from typing import Dict, List

from attr import dataclass
from discord import Thread
from discord.ext.commands import Context

from src.bot import bot, query_ai


class Dependencies:
    async def query_ai(self, prompt: str) -> str:
        return await query_ai(prompt)


@dataclass
class ChatMessage:
    role: str
    message: str


class ActiveChat:
    thread: Thread
    messages: List[ChatMessage]


chats: Dict[int, ActiveChat] = {}


def to_prompt(messages: List[ChatMessage]) -> str:
    new_messages = messages.copy()
    new_messages.append(ChatMessage("assistant", ""))
    return "\n".join(map(lambda x: f"${x.role}:${x.message}", new_messages))


async def get_completion(deps: Dependencies, messages: List[ChatMessage]) -> List[ChatMessage]:
    response = await deps.query_ai(to_prompt(messages))
    new_ai_message = ChatMessage("assistant", response)
    messages.append(new_ai_message)
    return messages


async def create_shrek_chat(dps: Dependencies, starting_message: str) -> List[ChatMessage]:
    system_message = ChatMessage("system", "You are shrek. You must act like shrek. You can never break character.")
    current_message = ChatMessage("user", starting_message)
    current_chat = [system_message, current_message]
    current_chat = await get_completion(dps, current_chat)
    return current_chat


@bot.command
async def shrek_chat(ctx: Context, starting_message):
    res = await ctx.send("Och, fine, laddie, let's jist get this talk started already!")
    thread = await res.create_thread(name="Shrek Chat")
    res = await create_shrek_chat(Dependencies(), starting_message)
    chat = ActiveChat()
    chat.messages = res
    chat.thread = thread
    chats[thread.id] = chat
    await thread.send(res[-1].message)


async def handle_message(message: discord.message):
    if message.thread.id in chats:
        chat = chats[message.thread.id]
        chat.messages.append(ChatMessage("user", message.content))
        res = await get_completion(Dependencies(), chat.messages)
        chat.messages = res
        await message.thread.send(res[-1].message)

register_hook(handle_message)