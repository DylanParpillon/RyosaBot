# db/crud.py
import json
from datetime import datetime, timezone
from typing import List, Tuple
from db.model import get_conn

def add_message(user: str, channel: str, content: str, when_iso: str | None = None):
    conn = get_conn()
    when_iso = when_iso or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    conn.execute(
        "INSERT INTO messages (user, channel, content, created_at) VALUES (?, ?, ?, ?)",
        (user, channel, content, when_iso),
    )
    conn.commit()

def get_recent_messages(user: str, channel: str) -> List[Tuple[str, str]]:
    """Retourne [(content, created_at_iso)] du plus récent au plus ancien."""
    conn = get_conn()
    cur = conn.execute(
        "SELECT content, created_at FROM messages WHERE user=? AND channel=? ORDER BY created_at DESC LIMIT 8",
        (user, channel),
    )
    return list(cur.fetchall())
def count_messages(user: str, channel: str) -> int:
    conn = get_conn()
    cur = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE user=? AND channel=?",
        (user, channel),
    )
    return int(cur.fetchone()[0])

def clear_user(user: str, channel: str) -> int:
    conn = get_conn()
    cur = conn.execute(
        "DELETE FROM messages WHERE user=? AND channel=?",
        (user, channel),
    )
    conn.commit()
    return cur.rowcount

def save_memory(user: str, channel: str, text: str, embedding: list[float]):
    conn = get_conn()
    conn.execute(
        "INSERT INTO memories(user, channel, text, embedding, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
        (user, channel, text, json.dumps(embedding)),
    )
    conn.commit()

def load_memories(user: str, channel: str, limit: int = 1000):
    cur = get_conn().execute(
        "SELECT text, embedding FROM memories WHERE user=? AND channel=? ORDER BY created_at DESC LIMIT ?",
        (user, channel, limit),
    )
    rows = []
    for txt, emb_json in cur.fetchall():
        rows.append((txt, json.loads(emb_json)))
    return rows
