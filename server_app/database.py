import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="murojaatlar_app.sqlite3"):
        db_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, db_name)
        self.create_table()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path, timeout=15)
        try:
            conn.execute("PRAGMA journal_mode=MEMORY")
            conn.execute("PRAGMA busy_timeout=15000")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_table(self):
        """Murojaatlarni saqlash uchun jadval yaratish."""
        query = """
        CREATE TABLE IF NOT EXISTS murojaatlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foydalanuvchi TEXT DEFAULT 'Anonim',
            shifrlangan_matn TEXT NOT NULL,
            fayl_yo_li TEXT,
            toifa TEXT DEFAULT 'Tahlil qilinmoqda',
            vaqt TEXT
        )
        """
        with self.connect() as conn:
            conn.execute(query)

    def add_murojaat(self, encrypted_text, file_path=None):
        """Yangi murojaatni bazaga qo'shish."""
        vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO murojaatlar (shifrlangan_matn, fayl_yo_li, vaqt) VALUES (?, ?, ?)"
        with self.connect() as conn:
            cursor = conn.execute(query, (encrypted_text, file_path, vaqt))
            return cursor.lastrowid

    def get_all_murojaatlar(self):
        """Barcha murojaatlarni admin panel uchun olish."""
        with self.connect() as conn:
            cursor = conn.execute("SELECT * FROM murojaatlar ORDER BY id DESC")
            return cursor.fetchall()

    def update_category(self, murojaat_id, category):
        """AI aniqlagan toifani bazada yangilash."""
        query = "UPDATE murojaatlar SET toifa = ? WHERE id = ?"
        with self.connect() as conn:
            conn.execute(query, (category, murojaat_id))
