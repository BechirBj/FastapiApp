# import uuid
# from fastapi.testclient import TestClient

# from app.main import app


# client = TestClient(app)


# def test_root():

#     response = client.get("/")

#     assert response.status_code == 200
#     assert response.json() == {
#         "Hello": "World"
#     }


# def test_create_user():

#     user = {
#         "Nom": "Test",
#         "Prenom": "User",
#         "Poste": "Developer",
#         "Salaire": 2500,
# "Email": f"test-{uuid.uuid4()}@example.com",
#         "Service": "IT"
#     }

#     response = client.post(
#         "/users",
#         json=user
#     )

#     assert response.status_code == 201

#     data = response.json()

#     assert data["Nom"] == "Test"
#     assert data["Prenom"] == "User"
#     assert data["Email"] == user["Email"]


# def test_get_non_existing_user():

#     response = client.get("/users/999999")

#     assert response.status_code == 404
#     assert response.json()["detail"] == "User not found"

import uuid

import httpx


BASE_URL = "http://localhost:8000"


def test_root():
    response = httpx.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert response.json() == {
        "Hello": "World"
    }


def test_create_user():
    user = {
        "Nom": "Test",
        "Prenom": "User",
        "Poste": "Developer",
        "Salaire": 2500,
        "Email": f"test-{uuid.uuid4()}@example.com",
        "Service": "IT"
    }

    response = httpx.post(
        f"{BASE_URL}/users",
        json=user
    )

    assert response.status_code == 201

    data = response.json()

    assert data["Nom"] == user["Nom"]
    assert data["Prenom"] == user["Prenom"]
    assert data["Email"] == user["Email"]


def test_get_non_existing_user():
    response = httpx.get(
        f"{BASE_URL}/users/999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"