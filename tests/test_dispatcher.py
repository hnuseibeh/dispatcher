from fastapi.testclient import TestClient
from ui.dispatcher.app import app

client = TestClient(app)

def test_create_task():
    payload = {"prompt": "Test task from pytest"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["prompt"] == payload["prompt"]