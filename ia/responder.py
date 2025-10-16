# ia/responder.py
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import numpy as np
from db.crud import load_memories


_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = os.getenv("BOT_SYSTEM_PROMPT")

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




EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
#async le fait de segmenté les recherches
async def semantic_search(query: str, user: str, channel: str, k: int = 5) -> list[str]:
    import asyncio
    q = np.array(await asyncio.to_thread(embed_text, query), dtype=np.float32)
    items = load_memories(user, channel, limit=1000)
    scored = []
    for it txt, emb inems:
        v = np.array(emb, dtype=np.float32)
        scored.append((txt, cosine(q, v)))
    scored.sort(key=lambda t: t[1], reverse=True)
    return [t[0] for t in scored[:k]]

def embed_text(text: str) -> list[float]:
    emb = _client.embeddings.create(model=EMBED_MODEL, input=text).data[0].embedding
    return emb

#sert a calculé les coeerance de vecteur
def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0: return 0.0
    return float(np.dot(a, b) / (na * nb))

