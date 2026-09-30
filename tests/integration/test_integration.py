import sqlite3

from app.database import get_connection, init_database


def test_database_initialization(tmp_path):

    database = tmp_path / "test.db"

    init_database(str(database))

    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='employes'
    """)

    table = cursor.fetchone()

    conn.close()

    assert table is not None


def test_insert_employee(tmp_path):

    database = tmp_path / "test.db"

    init_database(str(database))

    conn = get_connection(str(database))

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employes
        (Nom, Prenom, Poste, Salaire, Email, Service)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Ben Ali",
        "Ahmed",
        "Developer",
        2500,
        "ahmed@test.com",
        "IT"
    ))

    conn.commit()

    cursor.execute("""
        SELECT *
        FROM employes
        WHERE Email = ?
    """, ("ahmed@test.com",))

    employee = cursor.fetchone()

    conn.close()

    assert employee is not None
    assert employee["Nom"] == "Ben Ali"
    assert employee["Prenom"] == "Ahmed"
    assert employee["Salaire"] == 2500


def test_total(tmp_path):
    print("####### Testing the total #######")

    database = tmp_path / "test.db"

    init_database(str(database))

    conn = get_connection(str(database))
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employes
        (Nom, Prenom, Poste, Salaire, Email, Service)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Ben Ali",
        "Ahmed",
        "Developer",
        2500,
        "ahmed@test.com",
        "IT"
    ))

    conn.commit()

    cursor.execute("""
        SELECT SUM(Salaire)
        FROM employes
    """)

    total_salaire = cursor.fetchone()[0]

    conn.close()

    assert total_salaire == 2500
