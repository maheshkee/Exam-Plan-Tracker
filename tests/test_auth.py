def test_register_success(client):
    res = client.post("/auth/register", json={"email": "newuser@test.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json()["email"] == "newuser@test.com"
    assert "password_hash" not in res.json()

def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    res = client.post("/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    assert res.status_code == 400

def test_register_short_password(client):
    res = client.post("/auth/register", json={"email": "short@test.com", "password": "abc"})
    assert res.status_code == 422

def test_login_success(client):
    client.post("/auth/register", json={"email": "login@test.com", "password": "loginpass1"})
    res = client.post("/auth/login", json={"email": "login@test.com", "password": "loginpass1"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_wrong_password(client):
    res = client.post("/auth/login", json={"email": "testuser@test.com", "password": "wrongpass"})
    assert res.status_code == 401

def test_me_authenticated(client, auth_headers):
    res = client.get("/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["email"] == "testuser@test.com"

def test_me_unauthenticated(client):
    res = client.get("/auth/me")
    assert res.status_code == 401
