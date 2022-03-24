def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the sample app" in str(response.data)
    assert "<title>Welcome!</title>" in str(response.data)


def test_auth_login(client):
    # redirects to Cognito
    response = client.get("/login")
    assert response.status_code == 302


def test_private_logged_out(client):
    # 403 unauthorized
    response = client.get("/private")
    assert response.status_code == 403
