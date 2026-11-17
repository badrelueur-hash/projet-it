import os
import sqlite3
from datetime import datetime

# Chemin absolu : la base est toujours au meme endroit, peu importe d'ou on lance le script
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mesures.db")


def connexion():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA journal_mode=WAL")  # lecture (Flask) + ecriture (capteurs) en meme temps
    return conn


def maintenant():
    # Format unique pour tout le projet : 2026-11-17T14:32:10 (heure locale)
    return datetime.now().isoformat(timespec="seconds")


def init_db():
    conn = connexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mesures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capteur TEXT NOT NULL,
            type_mesure TEXT NOT NULL,
            valeur REAL NOT NULL,
            unite TEXT NOT NULL,
            horodatage TEXT NOT NULL
        )
    """)
    # Index : recherches rapides par type de mesure et par date
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_type_heure ON mesures (type_mesure, horodatage)"
    )
    conn.commit()
    conn.close()


def inserer(capteur, type_mesure, valeur, unite):
    conn = connexion()
    conn.execute(
        "INSERT INTO mesures (capteur, type_mesure, valeur, unite, horodatage) "
        "VALUES (?, ?, ?, ?, ?)",
        (capteur, type_mesure, valeur, unite, maintenant()),
    )
    conn.commit()
    conn.close()


def lire_tout(limite=1000):
    conn = connexion()
    lignes = conn.execute(
        "SELECT * FROM mesures ORDER BY id DESC LIMIT ?", (limite,)
    ).fetchall()
    conn.close()
    return lignes


def lire_periode(type_mesure, debut, fin):
    # debut / fin au format "2026-11-17T14:00:00"
    conn = connexion()
    lignes = conn.execute(
        "SELECT horodatage, valeur FROM mesures "
        "WHERE type_mesure = ? AND horodatage BETWEEN ? AND ? "
        "ORDER BY horodatage",
        (type_mesure, debut, fin),
    ).fetchall()
    conn.close()
    return lignes


def lire_dernieres(n=20):  # lien entre db.py et anomalies.py
    conn = connexion()
    lignes = conn.execute(
        "SELECT capteur, type_mesure, valeur, unite, horodatage "
        "FROM mesures ORDER BY id DESC LIMIT ?",
        (n,),
    ).fetchall()
    conn.close()
    return lignes


# ---------- Utilisateurs ----------

def init_users():
    conn = connexion()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('admin', 'operateur', 'observateur'))
        )
    """)
    conn.commit()
    conn.close()


def creer_user(username, password_hash, role):
    conn = connexion()
    conn.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    conn.commit()
    conn.close()


def get_user_par_id(user_id):
    conn = connexion()
    ligne = conn.execute(
        "SELECT id, username, password_hash, role FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return ligne


def get_user_par_nom(username):
    conn = connexion()
    ligne = conn.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()
    return ligne


if __name__ == "__main__":
    init_db()
    init_users()
    print("Base prete :", DB)