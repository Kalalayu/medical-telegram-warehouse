# tests/api/test_search.py
import pytest
from fastapi.testclient import TestClient
from api.main import app, get_db

client = TestClient(app)

def test_message_search():
    # 1. Fake database result with attribute access
    class FakeRow:
        def __init__(self, message_id, channel_name, text, created_at):
            self.message_id = message_id
            self.channel_name = channel_name
            self.text = text
            self.created_at = created_at

    fake_result = [
        FakeRow(1, "test_channel", "paracetamol is available", "2024-01-01")
    ]

    # 2. Mock db.execute().fetchall()
    class FakeResult:
        def fetchall(self):
            return fake_result

    class FakeDB:
        def execute(self, *args, **kwargs):
            return FakeResult()

    # 3. Override get_db dependency
    def fake_get_db():
        return FakeDB()

    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = lambda: FakeDB()


    # 4. Call API
    response = client.get("/api/search/messages?query=para&limit=5")
    data = response.json()

    # 5. Assertions
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["message_id"] == 1
    assert data[0]["channel_name"] == "test_channel"
    assert "paracetamol" in data[0]["text"]
