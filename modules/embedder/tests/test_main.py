from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_embed():
    response = client.post("/embed", json={"inputs": "Hello, world!"})
    assert response.status_code == 200
    assert len(response.json()["embeddings"]) > 0