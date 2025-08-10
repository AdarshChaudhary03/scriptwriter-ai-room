import sqlite3

DB_FILE = "scripts.db"

def init_db():
    """Create the scripts table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scripts (
            script_id TEXT PRIMARY KEY,
            genre TEXT,
            idea TEXT,
            characters TEXT,
            outline TEXT,
            dialogues TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(script_id,genre=None, idea=None, characters=None, outline=None, dialogues=None):
    """Insert or update a script entry in the DB."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO scripts (script_id, genre, idea, outline, dialogues, characters)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(script_id) DO UPDATE SET
                genre=COALESCE(?, genre),
                idea=COALESCE(?, idea),
                outline=COALESCE(?, outline),
                dialogues=COALESCE(?, dialogues),
                characters=COALESCE(?, characters)
        """, (script_id, genre, idea, outline, dialogues, characters, genre,idea,outline,dialogues,characters))

    conn.commit()
    conn.close()

def get_script_data(script_id):
    conn = sqlite3.connect("scripts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scripts WHERE script_id=?", (script_id,))
    row = cursor.fetchone()

    conn.close()
    return row
