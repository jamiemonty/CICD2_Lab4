# tests/test_users.py
import pytest

def user_payload(uid=1, name="Jamie", email="G00419525@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Jamie"

def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409  # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert r.status_code == 422  # pydantic validation error

@pytest.mark.parametrize("bad_email", ["not-an-email", "missingatsign.com", "@no-local-part.com", "user@.com", "user@site..com"])
def test_invalid_email_update_422(client, bad_email):
    # Create valid user
    client.post("/api/users", json=user_payload(uid=4))
    
    # Attempt to update with invalid email
    update_data = {"name": "InvalidEmail", "email": bad_email, "age": 30, "student_id": "S1234567"}
    r = client.put("/api/users/4", json=update_data)
    assert r.status_code == 422

def test_delete_then_404(client):
    client.post("/api/users", json=user_payload(uid=10))
    r1 = client.delete("/api/users/10")
    assert r1.status_code == 204
    r2 = client.delete("/api/users/10")
    assert r2.status_code == 404

def test_update_user_ok(client):
    client.post("/api/users", json=user_payload(uid=5))
    update_data = {"user_id": 5, "name": "James", "email": "jamiemonty@atu.ie", "age": 25, "student_id": "S1234567"}
    r = client.put("/api/users/5", json=update_data)
    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == 5
    assert data["name"] == "James"
    assert data["email"] == "jamiemonty@atu.ie"

def test_update_user_not_found_404(client):
    # Test updating a user that doesn't exist
    update_data = {"user_id": 67, "name": "johndope", "email": "johndoh67@atu.ie","age": 67, "student_id": "S1234567"}
    r = client.put("/api/users/67", json=update_data)
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()
