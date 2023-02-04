from typing import Dict, List

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from tests.unit.score.test_routes import BATCH_PATH, STREAM_PATH

TEST_STREAM_INPUT = [
    {"patient1": [0.038076]},
    {"patient2": [-0.001882]},
    {"patient3": [0.085299]},
    {"patient4": [-0.089063]},
    {"patient5": [0.005383]},
]

TEST_BATCH_INPUT = [
    {
        "patient1": [0.038076],
        "patient2": [-0.001882],
        "patient3": [0.085299],
        "patient4": [-0.089063],
        "patient5": [0.005383],
    },
    {
        "patient1": [0.057076],
        "patient2": [-0.004382],
        "patient3": [0.084569],
        "patient4": [-0.0894863],
        "patient5": [0.005833],
    },
]


@pytest.mark.parametrize("body", TEST_STREAM_INPUT)
def test_stream_score(client: TestClient, body: Dict):
    params = {"modelVersion": "v1", "includeModelVersion": True, "includeInput": True}
    response = client.post(STREAM_PATH, params=params, json=body)
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    _assert_stream_response(response=result)


@pytest.mark.parametrize("body", TEST_BATCH_INPUT)
def test_batch_score(client: TestClient, body: Dict):
    params = {"modelVersion": "v1", "includeModelVersion": True, "includeInput": True}
    response = client.post(BATCH_PATH, params=params, json=body)
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    _assert_stream_response(response=result)


def _assert_stream_response(response: List):
    assert isinstance(response, list)

    response_keys = {"patient", "inputData", "progression", "modelVersion"}
    assert response_keys == response[0].keys()
