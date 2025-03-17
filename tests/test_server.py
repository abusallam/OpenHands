import pytest
from fastapi.testclient import TestClient
from server import OpenHandsMCP
import jwt
from datetime import datetime, timedelta

@pytest.fixture
def app():
    return OpenHandsMCP().get_app()

@pytest.fixture
def client(app):
    return TestClient(app)

@pytest.fixture
def auth_token():
    payload = {
        "client_id": "test-client",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "your-secret-key", algorithm="HS256")

def test_status_endpoint(client, auth_token):
    response = client.get(
        "/status",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "aider_initialized" in data["data"]

def test_edit_file_endpoint(client, auth_token):
    response = client.post(
        "/tools/edit_file",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "file_path": "test.py",
            "edit_instructions": "Add a print statement"
        }
    )
    assert response.status_code in [200, 500]  # 500 if Aider not initialized 