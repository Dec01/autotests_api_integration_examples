import os
import pytest

from src.models.processings.request_processing import Requests, Domain


@pytest.fixture(autouse=True)
def domain():
    return Domain

@pytest.fixture(autouse=True)
def req():
    return Requests
