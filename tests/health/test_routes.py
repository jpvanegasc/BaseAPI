def test_health(client):
    response = client.get("health")
    assert response.status_code == 200


def test_ping(client):
    response = client.get("/health/ping")
    assert response.status_code == 200


def test_database(client):
    response = client.get("/health/database")
    assert response.status_code == 200
