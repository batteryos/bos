"""Base HTTP client for BOS API endpoints."""

import dataclasses
from collections import Counter

import requests

from bos.exceptions import APIError, AuthError, NotFoundError


class BaseClient:
    """Shared HTTP client with auth and error handling."""

    def __init__(self, tokens, endpoints, timeout=30):
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self.timeout = timeout
        self._tokens = tokens
        self.endpoints = endpoints

        # Validate all api_keys have tokens
        required_keys = {e["api_key"] for e in endpoints}
        missing = required_keys - tokens.keys()
        if missing:
            raise AuthError(
                f"Missing tokens for: {missing}. " f"Available: {set(tokens.keys())}"
            )

        # Default host and auth from most common across endpoints
        hosts = [e["host"] for e in endpoints]
        self.default_host = Counter(hosts).most_common(1)[0][0]
        keys = [e["api_key"] for e in endpoints]
        self.default_key = Counter(keys).most_common(1)[0][0]
        self.session.headers["Authorization"] = f"Token {tokens[self.default_key]}"

        # Per-endpoint overrides (entries that differ in host OR api_key)
        self.overrides = {}
        for entry in endpoints:
            if (
                entry["host"] != self.default_host
                or entry["api_key"] != self.default_key
            ):
                self.overrides[entry["endpoint"]] = entry

    def resolve(self, path):
        """Find host and auth overrides for a request path.

        Returns (host, auth_headers) where auth_headers is None when
        the default session token applies, or a dict with an
        Authorization header for endpoints using a different api_key.
        """
        if self.overrides:
            path_stripped = path.lstrip("/")
            for pattern, entry in self.overrides.items():
                prefix = pattern.lstrip("/").split("{")[0]
                if path_stripped.startswith(prefix):
                    host = entry["host"]
                    auth = None
                    if entry["api_key"] != self.default_key:
                        auth = {
                            "Authorization": f"Token {self._tokens[entry['api_key']]}"
                        }
                    return host, auth
        return self.default_host, None

    def prepare(self, path):
        """Build URL and per-request auth headers for a path."""
        host, auth = self.resolve(path)
        url = f"{host.rstrip('/')}/{path.lstrip('/')}"
        return url, auth

    def handle_response(self, resp):
        if resp.status_code == 404:
            raise NotFoundError(response=resp)
        if not resp.ok:
            try:
                detail = resp.json()
            except (ValueError, KeyError):
                detail = resp.text
            raise APIError(resp.status_code, str(detail), response=resp)
        if resp.status_code == 204 or not resp.content:
            return {}

        content_type = resp.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            return resp.json()

        # For binary data (ZIP, PDF, XLS, etc.) or plain text
        return resp.content

    @staticmethod
    def serialize(body, kwargs):
        """Build JSON payload from a request dataclass and/or **kwargs.

        - dataclass only: serialize fields, omit Nones
        - kwargs only: pass through as dict
        - both: dataclass fields merged with kwargs (kwargs win)
        - neither: return None
        """
        result = {}
        if body is not None:
            if dataclasses.is_dataclass(body):
                result = {
                    f.name: getattr(body, f.name)
                    for f in dataclasses.fields(body)
                    if getattr(body, f.name) is not None
                }
            elif isinstance(body, dict):
                result = body
        if kwargs:
            result.update(kwargs)
        return result or None

    def get(self, path, params=None):
        url, auth = self.prepare(path)
        resp = self.session.get(url, params=params, timeout=self.timeout, headers=auth)
        return self.handle_response(resp)

    def post(self, path, json_data=None):
        url, auth = self.prepare(path)
        resp = self.session.post(
            url, json=json_data, timeout=self.timeout, headers=auth
        )
        return self.handle_response(resp)

    def post_form(self, path, data=None, params=None):
        """POST with form-urlencoded content type."""
        url, auth = self.prepare(path)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if auth:
            headers.update(auth)
        resp = self.session.post(
            url, data=data, params=params, headers=headers, timeout=self.timeout
        )
        return self.handle_response(resp)

    def post_multipart(self, path, data=None, files=None):
        """POST with multipart/form-data (file uploads)."""
        url, auth = self.prepare(path)
        headers = {
            k: v for k, v in self.session.headers.items() if k.lower() != "content-type"
        }
        if auth:
            headers.update(auth)
        resp = requests.post(
            url, data=data, files=files, headers=headers, timeout=self.timeout
        )
        if resp.headers.get("Content-Type", "").startswith("application/"):
            if "json" in resp.headers["Content-Type"]:
                return self.handle_response(resp)
        if resp.status_code == 404:
            raise NotFoundError(response=resp)
        if not resp.ok:
            raise APIError(resp.status_code, response=resp)
        return resp.content

    def get_bytes(self, path, params=None):
        """GET that returns raw bytes (for file downloads like XLS)."""
        url, auth = self.prepare(path)
        resp = self.session.get(url, params=params, timeout=self.timeout, headers=auth)
        if resp.status_code == 404:
            raise NotFoundError(response=resp)
        if not resp.ok:
            raise APIError(resp.status_code, response=resp)
        return resp.content
