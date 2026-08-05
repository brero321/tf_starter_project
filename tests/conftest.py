import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))

import pytest
from unittest.mock import MagicMock

import example


@pytest.fixture
def mock_s3(monkeypatch):
    """Replace boto3.client('s3') with a mock for the duration of a test."""
    mock = MagicMock()
    monkeypatch.setattr(example.boto3, "client", lambda *args, **kwargs: mock)
    return mock


@pytest.fixture
def bucket_env(monkeypatch):
    """Set BUCKET_NAME for the duration of a test."""
    monkeypatch.setenv("BUCKET_NAME", "example-lambda-data-bucket")