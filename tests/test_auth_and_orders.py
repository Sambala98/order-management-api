from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.db.session import SessionLocal

client = TestClient(app)

def promote_user_to_admin(email: str):
    db = SessionLocal()
    try:
        db.execute(text("UPDATE users SET role='admin' WHERE email=:email"), {"email": email})
        db.commit()
    finally:
        db.close()

def test_rbac_user_and_admin_delete_flow():
    email = "testuser@test.com"
    password = "123456"

    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token_user = r.json()["access_token"]
    headers_user = {"Authorization": f"Bearer {token_user}"}

    r = client.post(
        "/orders",
        json={"customer_name": "Sudheer", "item_name": "Keyboard", "quantity": 2},
        headers=headers_user,
    )
    assert r.status_code == 201
    created = r.json()
    order_id = created["id"]

    r = client.get("/orders", headers=headers_user)
    assert r.status_code == 200
    orders = r.json()
    assert isinstance(orders, list)
    assert any(o["id"] == order_id for o in orders)

    r = client.delete(f"/orders/{order_id}", headers=headers_user)
    assert r.status_code == 403
    assert r.json()["detail"] == "Admin access required"

    promote_user_to_admin(email)

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token_admin = r.json()["access_token"]
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    r = client.delete(f"/orders/{order_id}", headers=headers_admin)
    assert r.status_code == 204