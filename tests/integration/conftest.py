from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        yield client
