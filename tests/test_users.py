import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.models import Base

TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
# hand the client to the test
        yield c
# --- teardown happens when the 'with' block exits ---
def test_create_user(client):
    r = client.post("/api/users",
json={"name":"Paul","email":"pl@atu.ie","age":25,"student_id":"S1234567"})
    assert r.status_code == 201

    
    #Why install from requirements.txt instead of ad‑hoc pip installs?
    #Doing it this way ensures that all dependencies are installed in the correct versions as specified in the requirements.txt file.
    #This avoids potential version conflicts and makes the environment reproducible.

    #What does coverage tell you that “all tests passed” doesn’t?
    #Coverage provides insight into how much of the codebase is actually being tested.

    #Why assert error paths (422/404/409) as well as happy paths?
    #Asserting error paths ensures that the application handles invalid inputs.

    #What signal does a green GitHub Action send to teammates?
    #A green GitHub Action indicates that the code has passed all tests and checks.


