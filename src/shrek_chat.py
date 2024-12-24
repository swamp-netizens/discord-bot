from logging import Logger
from typing import Dict, List

from attr import dataclass
from discord import Message, Thread
from discord.ext.commands import Bot, Cog, Context, command

from src.llm import LocalLlm, OpenRouterLlm

logger = Logger(__name__)


@dataclass
class ChatMessage:
    role: str
    message: str


class ActiveChat:
    thread: Thread
    messages: List[ChatMessage]


def to_prompt(messages: List[ChatMessage]) -> str:
    new_messages = messages.copy()
    new_messages.append(ChatMessage("assistant", ""))
    return "\n".join(map(lambda x: f"${x.role}:${x.message}", new_messages))


async def get_completion(deps: LocalLlm, messages: List[ChatMessage]) -> List[ChatMessage]:
    response = await deps.query_ai(to_prompt(messages))
    new_ai_message = ChatMessage("assistant", response)
    messages.append(new_ai_message)
    return messages


def create_shrek_chat() -> List[ChatMessage]:
    system_message = ChatMessage("system", "You are shrek. You must act like shrek. You can never break character.")
    current_message = ChatMessage("assistant", "Och, fine, laddie, let's jist get this talk started already!")
    current_chat = [system_message, current_message]
    return current_chat


class ShrekChat(Cog):
    chats: Dict[int, ActiveChat] = {}
    deps: LocalLlm
    def __init__(self, bot: Bot, deps):
        self.bot = bot
        self._last_member = None
        self.deps = deps

    @command(name="shrek")
    async def shrek_chat(self, ctx: Context):
        thread = await ctx.message.create_thread(name="Shrek Chat")
        res = create_shrek_chat()
        chat = ActiveChat()
        chat.messages = res
        chat.thread = thread
        self.chats[thread.id] = chat
        await thread.send(res[-1].message)

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == self.bot.user.id:
            return
        if message.channel and message.channel.id in self.chats:
            chat = self.chats[message.channel.id]
            chat.messages.append(ChatMessage("user", message.content))
            res = await get_completion(self.deps, chat.messages)
            chat.messages = res
            await message.channel.send(res[-1].message)



async def setup(bot):
    await bot.add_cog(ShrekChat(bot, OpenRouterLlm()))