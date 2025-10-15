import os
from twitchio.ext import commands
from dotenv import load_dotenv
from ia.responder import get_reply, semantic_search
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

        # pour evité les echos
        await self.handle_commands(message)

        author_name = getattr(getattr(message, "author", None), "name", "unknown")
        channel_name = getattr(getattr(message, "channel", None), "name", "unknown")
        content = (getattr(message, "content", "") or "").strip()
        print(f"[{channel_name}] {author_name}: {content}")
        # ignore si pas de texte utilisateur
        if not content or author_name == "unknown":
            return
    #chaque messages en segment
        if len(content) >= 20:
            from ia.responder import embed_text
            import asyncio
            vec = await asyncio.to_thread(embed_text, content)
            from db.crud import save_memory
            save_memory(author_name, channel_name, content, vec)
        #add des messages

        add_message(message.author.name.strip(), message.channel.name, content)

        if "ryosa" in message.content.lower():

            rows = get_recent_messages(author_name, channel_name)
            hist_lines = [f"[{when}] {author_name}: {txt}" for (txt, when) in rows]
            mem_texts = await semantic_search(content, author_name, channel_name, k=5)
            # On fabrique un contexte compact pour l’IA
            context_blocks = []
            if hist_lines:
                context_blocks.append("Historique récent:\n" + "\n".join(hist_lines))
            if mem_texts:
                context_blocks.append("Souvenirs pertinents:\n- " + "\n- ".join(mem_texts))
            prompt = content
            if context_blocks:
                prompt += "\n\n" + "\n\n".join(context_blocks)

            prompt = content + ("\n\n" + "\n\n".join(context_blocks) if context_blocks else "")
            response = await get_reply(prompt)
            await message.channel.send(f"@{author_name} {response}")
            print(f"@{message.author.name} {response}")
bot = Bot()