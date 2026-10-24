import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["free_access"] is True


def test_models_endpoint():
    response = client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Models exist even if unavailable
    ids = [m["id"] for m in data]
    assert "nexora-chat" in ids
    for m in data:
        assert m["is_free"] is True
        assert m["status"] in ["available", "unavailable", "disabled"]