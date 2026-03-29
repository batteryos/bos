"""Tests for request dataclasses and serialize."""

from dataclasses import dataclass
from typing import Optional

import pytest

from bos.base import BaseClient
from bos.calc.client import CalcClient
from bos.calc.config import ENDPOINTS as CALC_ENDPOINTS
from bos.calc.models import CalcCreate, DataObjectCreate
from bos.exceptions import AuthError


@dataclass
class SampleFilter:
    name: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[list] = None


class TestSerialize:
    def test_none_returns_none(self):
        assert BaseClient.serialize(None, {}) is None

    def test_dict_passthrough(self):
        assert BaseClient.serialize({"a": 1}, {}) == {"a": 1}

    def test_dataclass_omits_none(self):
        f = SampleFilter(name="Vistra")
        result = BaseClient.serialize(f, {})
        assert result == {"name": "Vistra"}
        assert "duration" not in result
        assert "category" not in result

    def test_dataclass_all_fields(self):
        f = SampleFilter(name="Vistra", duration=[2, 4], category="standalone")
        result = BaseClient.serialize(f, {})
        assert result == {
            "name": "Vistra",
            "duration": [2, 4],
            "category": "standalone",
        }

    def test_kwargs_only(self):
        result = BaseClient.serialize(None, {"custom_param": True})
        assert result == {"custom_param": True}

    def test_dataclass_plus_kwargs_merge(self):
        f = SampleFilter(name="Vistra")
        result = BaseClient.serialize(f, {"undocumented": 42})
        assert result == {"name": "Vistra", "undocumented": 42}

    def test_kwargs_override_dataclass(self):
        f = SampleFilter(name="Vistra")
        result = BaseClient.serialize(f, {"name": "NextEra"})
        assert result == {"name": "NextEra"}

    def test_empty_dataclass_empty_kwargs_returns_none(self):
        f = SampleFilter()
        assert BaseClient.serialize(f, {}) is None


class TestMultiKeyAuth:
    ENDPOINTS = [
        {"endpoint": "/foo/", "host": "https://a.com", "api_key": "KEY_A"},
        {"endpoint": "/bar/", "host": "https://a.com", "api_key": "KEY_A"},
        {"endpoint": "/baz/", "host": "https://b.com", "api_key": "KEY_B"},
    ]

    def test_default_auth_on_session(self, mock_session):
        tokens = {"KEY_A": "token-a", "KEY_B": "token-b"}
        BaseClient(tokens, self.ENDPOINTS)
        assert mock_session.headers["Authorization"] == "Token token-a"

    def test_default_endpoint_uses_session_auth(self, mock_session, mock_response):
        tokens = {"KEY_A": "token-a", "KEY_B": "token-b"}
        client = BaseClient(tokens, self.ENDPOINTS)
        mock_session.get.return_value = mock_response(json_data={})
        client.get("/foo/")
        _, kwargs = mock_session.get.call_args
        assert kwargs.get("headers") is None

    def test_override_endpoint_sends_per_request_auth(self, mock_session, mock_response):
        tokens = {"KEY_A": "token-a", "KEY_B": "token-b"}
        client = BaseClient(tokens, self.ENDPOINTS)
        mock_session.get.return_value = mock_response(json_data={})
        client.get("/baz/")
        _, kwargs = mock_session.get.call_args
        assert kwargs["headers"]["Authorization"] == "Token token-b"

    def test_override_endpoint_url_uses_correct_host(self, mock_session, mock_response):
        tokens = {"KEY_A": "token-a", "KEY_B": "token-b"}
        client = BaseClient(tokens, self.ENDPOINTS)
        mock_session.get.return_value = mock_response(json_data={})
        client.get("/baz/")
        args, _ = mock_session.get.call_args
        assert args[0].startswith("https://b.com")

    def test_missing_token_raises_auth_error(self, mock_session):
        tokens = {"KEY_A": "token-a"}
        with pytest.raises(AuthError, match="KEY_B"):
            BaseClient(tokens, self.ENDPOINTS)

    def test_post_multipart_uses_override_auth(self, mock_session, mock_response):
        from unittest.mock import patch

        tokens = {"KEY_A": "token-a", "KEY_B": "token-b"}
        client = BaseClient(tokens, self.ENDPOINTS)
        with patch("bos.base.requests.post") as mock_post:
            resp = mock_response(json_data={"ok": True})
            resp.headers = {"Content-Type": "application/json"}
            mock_post.return_value = resp
            client.post_multipart("/baz/", data={"x": 1})
            _, kwargs = mock_post.call_args
            assert kwargs["headers"]["Authorization"] == "Token token-b"


class TestCalcCreateIntegration:
    def test_create_calc_with_dataclass(self, mock_session, mock_response):
        client = CalcClient({"BOS_API": "test-token"}, CALC_ENDPOINTS)
        mock_session.post.return_value = mock_response(
            json_data={
                "slug": "new",
                "name": "Test",
                "iso": "ERCOT",
                "node": "HB_HOUSTON",
                "capacity": 100,
                "duration": 2,
            }
        )
        req = CalcCreate(name="Test")
        client.create_calc(req)
        call_json = mock_session.post.call_args[1].get("json")
        assert call_json["name"] == "Test"

    def test_create_data_object_with_dataclass(self, mock_session, mock_response):
        client = CalcClient({"BOS_API": "test-token"}, CALC_ENDPOINTS)
        mock_session.post.return_value = mock_response(
            json_data={"slug": "d1", "name": "My Data"}
        )
        client.create_data_object(DataObjectCreate(name="My Data"))
        call_json = mock_session.post.call_args[1].get("json")
        assert call_json == {"name": "My Data"}
