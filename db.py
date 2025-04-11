import sqlite3

def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS progress (
        user_id INTEGER,
        topic TEXT,
        correct INTEGER,
        total INTEGER
    )""")
    conn.commit()
    conn.close()

def update_progress(user_id, topic, correct):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM progress WHERE user_id=? AND topic=?", (user_id, topic))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE progress SET correct=correct+?, total=total+1 WHERE user_id=? AND topic=?",
                    (correct, user_id, topic))
    else:
        cur.execute("INSERT INTO progress (user_id, topic, correct, total) VALUES (?, ?, ?, 1)",
                    (user_id, topic, correct))
    conn.commit()
    conn.close()
