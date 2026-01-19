# from fastapi.testclient import TestClient
from api.main import app
from fastapi.testclient import TestClient
from api.main import app, get_db   # THIS WORKS NOW


client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
