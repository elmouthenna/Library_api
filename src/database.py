import sqlite3
from pathlib import Path

# Vérifie le chemin du fichier SQLite
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "books.db"

def get_connection():
    """Ouvre une connexion à la base SQLite."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Crée la table 'books' si elle n'existe pas."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
    """)

    conn.commit()
    conn.close()
