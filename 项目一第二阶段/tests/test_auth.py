import json


def test_register_success(client):
    res = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "PassWord123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["code"] == 201
    assert data["data"]["user"]["username"] == "alice"
    assert "access_token" in data["data"]


def test_register_duplicate(client):
    client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "PassWord123"
    })
    res = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice2@example.com",
        "password": "PassWord123"
    })
    assert res.status_code == 400


def test_register_missing_fields(client):
    res = client.post("/api/auth/register", json={
        "username": "alice"
    })
    assert res.status_code == 400


def test_login_success(client, auth_headers):
    assert auth_headers is not None
    res = client.post("/api/auth/login", json={
        "username": "tester",
        "password": "TestPass123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["code"] == 200
    assert "access_token" in data["data"]


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "PassWord123"
    })
    res = client.post("/api/auth/login", json={
        "username": "bob",
        "password": "WrongPass123"
    })
    assert res.status_code == 401


def test_login_not_found(client):
    res = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "PassWord123"
    })
    assert res.status_code == 401


def test_get_current_user(client, auth_headers):
    res = client.get("/api/auth/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["data"]["username"] == "tester"


def test_get_current_user_no_token(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401