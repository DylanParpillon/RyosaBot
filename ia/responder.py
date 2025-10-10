# ia/responder.py
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = os.getenv("BOT_SYSTEM_PROMPT",
    "Tu es Ryosa, un bot Twitch utile, concis, poli et fun. "
    "Réponds en français. Si une question est illégale ou dangereuse, refuse poliment."
)

async def get_reply(prompt: str) -> str:
    """
    Appel modèle en thread pour ne pas bloquer l'event loop TwitchIO.
    """
    def _call():
        try:
            resp = _client.chat.completions.create(
                model=_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[AI error] {e}"
    return await asyncio.to_thread(_call)
