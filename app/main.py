from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

from app.database import get_connection, init_database


app = FastAPI(
    title="Employee API",
    description="Simple FastAPI application for managing employees",
    version="1.0.0"
)

DATABASE = "entreprise.db"
init_database(DATABASE)

class UserCreate(BaseModel):
    Nom: str
    Prenom: str
    Poste: str
    Salaire: float
    Email: str
    Service: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def users():

    conn = get_connection(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employes
    """)

    users = cursor.fetchall()

    conn.close()

    return [dict(user) for user in users]

@app.post("/users", status_code=201)
def create_user(user: UserCreate):

    conn = get_connection(DATABASE)

    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO employes
            (
                Nom,
                Prenom,
                Poste,
                Salaire,
                Email,
                Service
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user.Nom,
            user.Prenom,
            user.Poste,
            user.Salaire,
            user.Email,
            user.Service
        ))

        conn.commit()

        user_id = cursor.lastrowid

        return {
            "id": user_id,
            **user.model_dump()
        }

    except sqlite3.IntegrityError as error:

        conn.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:

        conn.close()


@app.get("/users/{user_id}")
def get_user(user_id: int):

    conn = get_connection(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM employes
        WHERE Id = ?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return dict(user)

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):

    conn = get_connection(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employes
        WHERE Id = ?
    """, (user_id,))

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return None