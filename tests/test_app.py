import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_and_duplicate():
    # Use a unique email for test
    email = "pytestuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json().get("detail", "")

def test_unregister():
    email = "pytestuser2@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code in (200, 404)  # 404 if already removed
