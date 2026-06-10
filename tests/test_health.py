from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """
    Verify that the health check endpoint is working correctly.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Startup Risk Analyzer API is running"
    }