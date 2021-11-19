import pathlib
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


def test_malformed_task():
    global job_id

    with open("tests/jobs/malformed_schemas/malformed_task.json", "r") as fp:
        job = json.loads(fp.read())

    # XXX see if it is called json (analogous to linka)
    response = client.post("/api/v1/jobs/", json=job)
    assert response.status_code == 422


def test_malformed_storage():
    global job_id

    with open("tests/jobs/malformed_schemas/malformed_storage.json", "r") as fp:
        job = json.loads(fp.read())

    # XXX see if it is called json (analogous to linka)
    response = client.post("/api/v1/jobs/", json=job)
    assert response.status_code == 422


def test_malformed_callback():
    global job_id

    with open("tests/jobs/malformed_schemas/malformed_callback.json", "r") as fp:
        job = json.loads(fp.read())

    # XXX see if it is called json (analogous to linka)
    response = client.post("/api/v1/jobs/", json=job)
    assert response.status_code == 422
