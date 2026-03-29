"""Shared test fixtures for BOS API wrapper tests."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_session():
    """Mock requests.Session with configurable responses."""
    with patch("bos.base.requests.Session") as mock_cls:
        session = mock_cls.return_value
        session.headers = {}
        yield session


@pytest.fixture
def mock_response():
    """Factory for mock HTTP responses."""

    def _make(status_code=200, json_data=None, content=b"", ok=True):
        resp = MagicMock()
        resp.status_code = status_code
        resp.ok = ok
        resp.content = content or (b"{}" if json_data is not None else b"")
        resp.json.return_value = json_data if json_data is not None else {}
        resp.text = str(json_data) if json_data else ""
        return resp

    return _make
