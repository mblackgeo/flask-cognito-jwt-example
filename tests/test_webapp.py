def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the sample app" in str(response.data)
    assert "<title>Welcome!</title>" in str(response.data)


def test_private_logged_out(client):
    response = client.get("/private")
    assert response.status_code == 302


def test_private_logged_in():
    pass
    # TODO
    # mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    # assert "<title>This is a protected page!</title>" in str(response.data)
    # assert "Well done, you have authenticated successfully" in str(response.data)
