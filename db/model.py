# db/model.py
import sqlite3

connection = sqlite3.connect("memory.db")
print(connection.total_changes)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user       TEXT NOT NULL,
    channel    TEXT NOT NULL,
    content    TEXT NOT NULL,
    created_at TEXT NOT NULL
);
""")
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_messages_user_channel_created
ON messages(user, channel, created_at);
""")
connection.commit()
def get_conn() -> sqlite3.Connection:
    return connection