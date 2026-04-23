import pytest
from fastapi.testclient import TestClient
from src.app import app as fastapi_app

@pytest.fixture
def client():
    """Fixture to provide a FastAPI TestClient for testing the app."""
    return TestClient(fastapi_app)