"""API tests using FastAPI's TestClient (httpx under the hood).

Some tests target the deliberately planted problems and are expected to
FAIL on the fresh, unmodified project.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import repository


@pytest.fixture(autouse=True)
def clear_repository():
    """Reset the shared repository before each test for isolation."""
    repository._items.clear()
    repository._next_id = -1
    yield


@pytest.fixture
def client():
    """Provide a TestClient bound to the FastAPI app."""
    return TestClient(app)


def test_health(client):
    """The health endpoint returns a simple ok status."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_bookmark(client):
    """POST /bookmarks stores and echoes back the bookmark."""
    payload = {"url": "https://example.com", "title": "Example", "tags": ["web"]}
    resp = client.post("/bookmarks", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["url"] == "https://example.com"
    assert "id" in body


def test_list_bookmarks(client):
    """GET /bookmarks lists all stored bookmarks."""
    client.post("/bookmarks", json={"url": "https://a.com", "title": "A", "tags": []})
    client.post("/bookmarks", json={"url": "https://b.com", "title": "B", "tags": []})
    resp = client.get("/bookmarks")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_existing_bookmark(client):
    """GET /bookmarks/{id} returns a stored bookmark."""
    created = client.post(
        "/bookmarks", json={"url": "https://a.com", "title": "A", "tags": []}
    ).json()
    resp = client.get(f"/bookmarks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "A"


def test_first_bookmark_has_id_one(client):
    """Planted problem 4: the first created bookmark should have id 1."""
    created = client.post(
        "/bookmarks", json={"url": "https://a.com", "title": "A", "tags": []}
    ).json()
    assert created["id"] == 1  # currently fails: first id is 0


def test_get_missing_returns_404(client):
    """Planted problem 2: a missing id should return 404, not 200/null."""
    resp = client.get("/bookmarks/999")
    assert resp.status_code == 404  # currently fails: returns 200 with null


def test_delete_bookmark_returns_204(client):
    """Planted problem 3: DELETE should remove the bookmark and return 204."""
    created = client.post(
        "/bookmarks", json={"url": "https://a.com", "title": "A", "tags": []}
    ).json()
    resp = client.delete(f"/bookmarks/{created['id']}")
    assert resp.status_code == 204  # currently fails: raises NotImplementedError


def test_search_by_tag(client):
    """Planted problem 6: GET /bookmarks/search?tag=... should filter by tag."""
    client.post(
        "/bookmarks", json={"url": "https://a.com", "title": "A", "tags": ["Python"]}
    )
    resp = client.get("/bookmarks/search", params={"tag": "python"})
    assert resp.status_code == 200  # currently fails: route is missing
    assert len(resp.json()) == 1  # also depends on planted problem 1 fix


def test_create_rejects_invalid_url(client):
    """Planted problem 5: a non-http(s) url should be rejected with 422."""
    payload = {"url": "ftp://nope", "title": "Bad", "tags": []}
    resp = client.post("/bookmarks", json=payload)
    assert resp.status_code == 422  # currently fails: no url validation


def test_create_rejects_empty_url(client):
    """Planted problem 5: an empty url should be rejected with 422."""
    payload = {"url": "", "title": "Empty", "tags": []}
    resp = client.post("/bookmarks", json=payload)
    assert resp.status_code == 422  # currently fails: no url validation
