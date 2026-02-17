import sqlite3

class Database:
    def __init__(self, db_path="database/bot_data.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Table for group settings
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
            chat_id INTEGER PRIMARY KEY,
            title TEXT,
            welcome_text TEXT DEFAULT 'Welcome {name} to {group}!',
            rules TEXT DEFAULT 'No rules set.',
            added_by INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        # Table for global stats
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INTEGER
        )''')
        self.conn.commit()

    def get_group(self, chat_id):
        self.cursor.execute("SELECT * FROM groups WHERE chat_id=?", (chat_id,))
        return self.cursor.fetchone()

    def update_group(self, chat_id, title, added_by):
        self.cursor.execute("INSERT OR REPLACE INTO groups (chat_id, title, added_by) VALUES (?, ?, ?)", 
                            (chat_id, title, added_by))
        self.conn.commit()

    def set_welcome(self, chat_id, text):
        self.cursor.execute("UPDATE groups SET welcome_text=? WHERE chat_id=?", (text, chat_id))
        self.conn.commit()

    def set_rules(self, chat_id, text):
        self.cursor.execute("UPDATE groups SET rules=? WHERE chat_id=?", (text, chat_id))
        self.conn.commit()

db = Database()
