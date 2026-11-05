import os
import sqlite3
import json

def init_db() :
    db = sqlite3.connect("db.db")
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            name TEXT PRIMARY KEY,
            data TEXT NOT NULL DEFAULT '{}'
    )
    """)

def log_change(user_id, data) :
    db = sqlite3.connect("db.db")
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO logs (
            name, data
        )
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET
            data = excluded.data
    """, (user_id, json.dumps(data, ensure_ascii = False)))
    db.commit()

def log_view(user_id) :
    db = sqlite3.connect("db.db")
    cursor = db.cursor()

    cursor.execute("""
        SELECT data FROM logs WHERE name = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result is None :
        data = {}
    else :
        data = json.loads(result[0])
    print(data)

    return data