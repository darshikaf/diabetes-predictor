from pathlib import Path
import tempfile
from typing import Dict, List

from fastapi.testclient import TestClient
import pytest

from app.main import app

@pytest.fixture
def data_dir() -> Path:
    return Path(__file__).parent / "data"

@pytest.fixture
def path_prefix() -> str:
    return "/diabetes-detector"

@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as client:
        yield client

@pytest.fixture
def valid_stream_input() -> Dict:
    return {"patient1": [0.03807591]}

@pytest.fixture
def valid_stream_output() -> List:
    return [{'patient': 'patient1', 'progression': 188.64312218975726}]

@pytest.fixture
def valid_batch_input() -> Dict:
    return {"patient1": [0.03807591], "patient2": [0.03807595]}

@pytest.fixture
def valid_batch_output() -> List:
    return [
    {
        "patient": "patient1",
        "progression": 188.64312218975726
    },
    {
        "patient": "patient2",
        "progression": 188.64315971927172
    }
]
