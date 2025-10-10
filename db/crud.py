# db/crud.py
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
        "SELECT content, created_at FROM messages WHERE user=? AND channel=? ORDER BY created_at DESC ",
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
