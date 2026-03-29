"""Tests for bos.auth -- token resolution."""

import os
from unittest.mock import patch

import pytest

from bos.auth import resolve_token
from bos.exceptions import AuthError


class TestResolveToken:
    def test_explicit_token(self):
        assert resolve_token("my-token") == "my-token"

    def test_env_var(self):
        with patch.dict(os.environ, {"BOS_API": "env-token"}):
            assert resolve_token() == "env-token"

    def test_credentials_file(self, tmp_path):
        creds = tmp_path / ".bos" / "credentials"
        creds.parent.mkdir(parents=True)
        creds.write_text("file-token\n")
        with patch("bos.auth.Path.home", return_value=tmp_path):
            with patch.dict(os.environ, {}, clear=True):
                os.environ.pop("BOS_API", None)
                assert resolve_token() == "file-token"

    def test_no_token_raises(self, tmp_path):
        with patch("bos.auth.Path.home", return_value=tmp_path):
            with patch.dict(os.environ, {}, clear=True):
                os.environ.pop("BOS_API", None)
                with pytest.raises(AuthError):
                    resolve_token()

    def test_explicit_takes_precedence_over_env(self):
        with patch.dict(os.environ, {"BOS_API": "env-token"}):
            assert resolve_token("explicit") == "explicit"
