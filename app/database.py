import sqlite3


DATABASE = "entreprise.db"


def get_connection(database: str = DATABASE):
    conn = sqlite3.connect(
        database,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_database(database: str = DATABASE):
    conn = get_connection(database)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employes (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nom TEXT NOT NULL,
            Prenom TEXT NOT NULL,
            Poste TEXT NOT NULL,
            Salaire REAL CHECK(Salaire > 0),
            Email TEXT UNIQUE,
            date_embauche DATE DEFAULT CURRENT_DATE,
            Service TEXT NOT NULL,
            est_actif BOOLEAN DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()