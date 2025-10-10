import os

from twitchio.ext import commands
from openai import OpenAI

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.getenv("TWITCH_OAUTH_TOKEN"),
            prefix="!",
            initial_channels=[os.getenv("TWITCH_CHANNEL")]
        )

    async def event_ready(self):
        print(f"✅ Ryosa est connecté en tant que {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        if "ryosa" in message.content.lower():
            response = await get_response(message.content)
            await message.channel.send(f"@{message.author.name} {response}")

bot = Bot()