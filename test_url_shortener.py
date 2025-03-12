import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    response = client.post("/shorten", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_url" in data

def test_expand_url(client):
    shorten_resp = client.post("/shorten", json={"long_url": "https://example.com"})
    short_url = shorten_resp.get_json()["short_url"]

    expand_resp = client.get(f"/expand/{short_url}")
    assert expand_resp.status_code == 302

def test_expired_url(client):
    shorten_resp = client.post("/shorten", json={"long_url": "https://example.com", "expires_in": 1})
    short_url = shorten_resp.get_json()["short_url"]

    import time
    time.sleep(2)

    expand_resp = client.get(f"/expand/{short_url}")
    assert expand_resp.status_code == 410

def test_url_stats(client):
    shorten_resp = client.post("/shorten", json={"long_url": "https://example.com"})
    short_url = shorten_resp.get_json()["short_url"]

    stats_resp = client.get(f"/stats/{short_url}")
    assert stats_resp.status_code == 200
    assert "access_count" in stats_resp.get_json()
