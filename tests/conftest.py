import pytest


def pytest_addoption(parser):
    parser.addoption("--job_path", action="store")


@pytest.fixture
def job_path(request):
    return request.config.getoption("--job_path")
