import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mongomock
from unittest.mock import patch
import pytest

from app import create_app


@pytest.fixture(scope="session")
def app():
    with patch("pymongo.MongoClient", mongomock.MongoClient):
        app = create_app("testing")
        app.testing = True
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app import db
    return db


@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "TestPass123"
    })
    res = client.post("/api/auth/login", json={
        "username": "tester",
        "password": "TestPass123"
    })
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def survey_id(client, auth_headers):
    res = client.post("/api/surveys", json={
        "title": "测试问卷",
        "description": "用于测试的问卷",
        "settings": {}
    }, headers=auth_headers)
    return res.get_json()["data"]["id"]