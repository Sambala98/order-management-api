from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login_create_order():
    email = "testuser@test.com"
    password = "123456"

    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/orders", json={
        "customer_name": "Sudheer",
        "item_name": "Keyboard",
        "quantity": 2
    }, headers=headers)

    assert r.status_code == 201
    data = r.json()
    assert data["customer_name"] == "Sudheer"
    assert data["item_name"] == "Keyboard"
    assert data["quantity"] == 2
    assert "id" in data