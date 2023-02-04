from fastapi import status
from fastapi.testclient import TestClient
import pytest

from app.constants import PATH_PREFIX
from app.score.routes import SCORE_PREFIX

SCORE_PATH = PATH_PREFIX + SCORE_PREFIX
STREAM_PATH = f"{SCORE_PATH}/stream"
BATCH_PATH = f"{SCORE_PATH}/batch"


@pytest.fixture
def invalid_input() -> str:
    return {"patient1": ["0.03807591"]}


@pytest.fixture
def invalid_input_error_message() -> str:
    return '{"detail":"InvalidInput: All inputs must be of datatype List[float]."}'


def test_stream_score_minimal(client: TestClient, valid_stream_input, valid_stream_output):
    params = {"modelVersion": "v1"}
    response = client.post(STREAM_PATH, params=params, json=valid_stream_input)
    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert results == valid_stream_output


def test_stream_score(client: TestClient, valid_stream_input, valid_stream_output):
    params = {"modelVersion": "v1", "includeModelVersion": True, "includeInput": True}
    response = client.post(STREAM_PATH, params=params, json=valid_stream_input)
    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    valid_stream_output[0]["modelVersion"] = "v1"
    valid_stream_output[0]["inputData"] = valid_stream_input["patient1"][0]
    assert results == valid_stream_output


def test_batch_score_minimal(client: TestClient, valid_batch_input, valid_batch_output):
    params = {"modelVersion": "v1"}
    response = client.post(BATCH_PATH, params=params, json=valid_batch_input)
    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert results == valid_batch_output


def test_invalid_model_version(client: TestClient, valid_stream_input):
    params = {"modelVersion": "invalid"}
    response = client.post(STREAM_PATH, params=params, json=valid_stream_input)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.text == '{"detail":"Model version does not exist. InvalidModelVersion: invalid"}'


def test_batch_input_stream_endpoint(client: TestClient, valid_batch_input):
    params = {"modelVersion": "v1"}
    response = client.post(STREAM_PATH, params=params, json=valid_batch_input)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.text == '{"detail":"InvalidInput: Use v1/score/batch endpoint for batch processing."}'


def test_invalid_input_data_type_str(client: TestClient, invalid_input_error_message):
    params = {"modelVersion": "v1"}
    input_data = {"patient1": ["0.03807591"]}
    response = client.post(STREAM_PATH, params=params, json=input_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.text == invalid_input_error_message


def test_invalid_input_data_type_float(client: TestClient, invalid_input_error_message):
    params = {"modelVersion": "v1"}
    input_data = {"patient1": 0.03807591}
    response = client.post(STREAM_PATH, params=params, json=input_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.text == invalid_input_error_message
