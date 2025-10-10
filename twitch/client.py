import os
from twitchio.ext import commands
from dotenv import load_dotenv
from ia.responder import get_reply
from db.crud import add_message, get_recent_messages

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
        content = (message.content or "").strip()

        author_name = getattr(getattr(message, "author", None), "name", "unknown")
        channel_name = getattr(getattr(message, "channel", None), "name", "unknown")
        content = (getattr(message, "content", "") or "").strip()
        print(f"[{channel_name}] {author_name}: {content}")
        # ignore si pas de texte utilisateur
        if not content or author_name == "unknown":
            return

        if "ryosa" in message.content.lower():
            add_message(message.author.name.strip(), message.channel.name, content)
            #UNIQUEMENT POUR LUI REDONNER LES 8 DERNIER MESSAGES DE CONTEXT DE CETTE PERSONNE
            rows = get_recent_messages(message.author.name, message.channel.name)

            # On fabrique un contexte compact pour l’IA
            hist_lines = []
            for txt, when_iso in rows:
                hist_lines.append(f"[{when_iso}] {message.author.name}: {txt}")
            extra_context = "Historique récent de l'utilisateur dans ce chat:\n" + "\n".join(hist_lines)

            response = await get_reply(message.content + "\n\n" + extra_context)
            await message.channel.send(f"{response}")
            print(f"@{message.author.name} {response}")
bot = Bot()