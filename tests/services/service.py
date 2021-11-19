import os
import pathlib
import pytest
import json

from fastapi.testclient import TestClient

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


def test_create(job_path):
    global job_id

    with open(job_path, "r") as fp:
        job = json.loads(fp.read())

    # XXX see if it is called json (analogous to linka)
    response = client.post("/api/v1/jobs/", json=job)
    assert response.status_code == 200

    job_id = response.json()["id"]


# Returns True when job is finished
@pytest.mark.timeout(5)
def test_get():
    status = ""
    while status != "finished":
        response = client.get(f"/api/v1/jobs/{job_id}")
        assert response.status_code == 200
        status = response.json()["status"]

    assert response.status_code == 200
    assert response.json()["status"] == "finished"

    result = response.json()["result"]

    assert os.path.exists(storage_path)
    assert {"path": storage_path} == result

    assert os.path.exists(callback_path)
    with open(callback_path, "r") as fp:
        callback_content = json.loads(fp.read())
    assert callback_content == {"path": storage_path}


def test_list():
    response = client.get("/api/v1/jobs")
    assert response.status_code == 200

    job_ids = response.json()
    assert len(job_ids) == 1
    assert job_ids[0] == job_id


def test_cancel():
    response = client.delete(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200

    response = client.get("/api/v1/jobs")
    assert response.status_code == 200
    job_ids = response.json()
    assert len(job_ids) == 0
