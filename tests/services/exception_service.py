import pathlib
import json
import pytest
import os

from fastapi.testclient import TestClient

from dragonscales.schemas import Status

storage_path = "/tmp/dragonscale.storage"
callback_path = "/tmp/dragonscale.callback"


def setup_module():
    global client

    pathlib.Path(storage_path).unlink(missing_ok=True)
    pathlib.Path(callback_path).unlink(missing_ok=True)

    from dragonscales import services

    client = TestClient(services.app)


def teardown_module():
    pathlib.Path(storage_path).unlink(missing_ok=True)
    pathlib.Path(callback_path).unlink(missing_ok=True)


@pytest.mark.timeout(5)
def test_task_exception():
    global job_id
    global response

    with open("tests/jobs/exceptions/exception_task.json", "r") as fp:
        job = json.loads(fp.read())

    response = client.post("/api/v1/jobs/", json=job)
    assert response.status_code == 200
    job_id = response.json()["id"]

    status = ""
    while status != Status.FAILED:
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        status = response.json()["status"]

    assert response.json()["status"] == Status.FAILED


def test_callback_exception():
    assert os.path.exists(callback_path)
    with open(callback_path, "r") as fp:
        callback_content = json.loads(fp.read())
    assert callback_content["info"] != None
    assert callback_content["status"] == Status.FAILED
    assert callback_content["result"] == None
