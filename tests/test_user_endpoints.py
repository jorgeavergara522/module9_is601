from fastapi.testclient import TestClient
from uuid import uuid4
from app.main import app

client = TestClient(app)

def unique_creds():
    u = f"user_{uuid4().hex[:8]}"
    e = f"{u}@example.com"
    p = "Str0ngP@ss!"
    return u, e, p

def test_register_user_success():
    username, email, password = unique_creds()
    resp = client.post("/users/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["username"] == username
    assert data["email"] == email
    assert "password" not in data and "password_hash" not in data

def test_register_user_bad_email_422():
    username, _, password = unique_creds()
    resp = client.post("/users/register", json={
        "username": username,
        "email": "not-an-email",
        "password": password
    })
    assert resp.status_code == 422

def test_register_duplicate_username_conflict():
    username, email1, password = unique_creds()
    # first create
    r1 = client.post("/users/register", json={
        "username": username, "email": email1, "password": password
    })
    assert r1.status_code in (200, 201)
    # second with same username but different email
    email2 = f"dup_{uuid4().hex[:8]}@example.com"
    r2 = client.post("/users/register", json={
        "username": username, "email": email2, "password": password
    })
    # expect 400/409 depending on your handler
    assert r2.status_code in (400, 409, 422)

def test_login_success_then_get_user():
    username, email, password = unique_creds()
    r = client.post("/users/register", json={
        "username": username, "email": email, "password": password
    })
    assert r.status_code in (200, 201)
    user_id = r.json()["id"]

    # login endpoint should accept username or email per your design; adjust if needed
    login = client.post("/users/login", json={"username": username, "password": password})
    assert login.status_code in (200, 201, 204) or login.status_code == 200

    # fetch user by id
    g = client.get(f"/users/{user_id}")
    assert g.status_code == 200
    data = g.json()
    assert data["id"] == user_id
    assert data["username"] == username
    assert data["email"] == email
