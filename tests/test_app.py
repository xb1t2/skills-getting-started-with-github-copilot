import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Soccer Team"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/participants?email={email}")
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response3.status_code == 200
    assert f"Unregistered {email}" in response3.json()["message"]
    # Unregister again should fail
    response4 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response4.status_code == 404

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/participants?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_invalid_participant():
    response = client.delete("/activities/Soccer Team/participants?email=notfound@mergington.edu")
    assert response.status_code == 404
