import os
from twitchio.ext import commands
from dotenv import load_dotenv
from ia.responder import get_reply
load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.getenv("TWITCH_OAUTH_TOKEN"),
            prefix="!",
            initial_channels=[os.getenv("TWITCH_CHANNEL")],
        )
    async def event_ready(self):
        print(f"✅ Ryosa est connecté en tant que {self.nick}")

    async def event_message(self, message):
        print(f"{message.author.name}: {message.content}")
        if "ryosa" in message.content.lower():
            response = await get_reply(message.content)
            await message.channel.send(f"@{message.author.name} {response}")
            print(f"@{message.author.name} {response}")
bot = Bot()