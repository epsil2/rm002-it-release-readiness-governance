"""Contract tests for the health endpoint and the items API."""

from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_reports_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"].endswith("-backend")


def test_items_endpoint_lists_seeded_item() -> None:
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()["items"]]
    assert "first item" in names


def test_create_item_returns_created_payload() -> None:
    response = client.post("/api/v1/items", json={"name": "second item"})
    assert response.status_code == 201
    assert response.json()["name"] == "second item"
