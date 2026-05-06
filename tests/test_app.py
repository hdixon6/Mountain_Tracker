from app.main import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
    
def test_mountain_detail_contains_back_link():
    client = app.test_client()
    response = client.get("/mountain/1")
    assert b'href="/"' in response.data

