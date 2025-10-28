
import sqlite3
from datetime import datetime

DB = "posts.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, date TEXT, title TEXT, price TEXT, link TEXT, short_link TEXT, channel TEXT)''')
    conn.commit()
    conn.close()

def log_post(title, price, link, short_link, channel):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO posts (date, title, price, link, short_link, channel) VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.utcnow().isoformat(), title, price, link, short_link, channel))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized")
