from itertools import tee
from random import sample
from explicit_content_api.routers.http_nudenet import router
from fastapi.testclient import TestClient
from typing import Callable
from pathlib import Path
import os

client = TestClient(router)


def test_simple_router(load_test_images: Callable):
    """Simple router test"""
    sample_image = load_test_images[0]
    response = client.post(
        "/api/image-classifer/",
        files=sample_image
    )
    assert response.status_code == 200