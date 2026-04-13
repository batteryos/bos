"""BOS API token resolution."""

import os
from pathlib import Path
import requests

from bos.exceptions import AuthError, APIError


def resolve_token(token=None):
    """Resolve BOS API token.

    Order: explicit arg > BOS_API env var > ~/.bos/credentials file.
    """
    if token:
        return token
    token = os.environ.get("BOS_API")
    if token:
        return token
    creds_path = Path.home() / ".bos" / "credentials"
    if creds_path.exists():
        return creds_path.read_text().strip()
    raise AuthError(
        "No BOS API token found. Please use BOSAuth to complete the OTP verification flow."
    )


def resolve_tokens(token=None):
    """Resolve all API credentials.

    Args:
        token: str (single token for all keys), dict (key_name -> token),
               or None (resolve from env/file).

    Returns dict of key_name -> resolved token.
    """
    if isinstance(token, dict):
        return token
    base = resolve_token(token)
    return {"BOS_API": base}


class BOSAuth:
    """Handles the CLI OTP authentication flow to obtain a BOS API token."""

    def __init__(self, base_url="https://batteryos.com/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"

    def request_otp(self, email: str):
        """Request an OTP be sent to the provided email."""
        url = f"{self.base_url}/auth/cli/request/"
        resp = self.session.post(url, json={"email": email})
        if not resp.ok:
            raise APIError(resp.status_code, resp.text, response=resp)
        return resp.json()

    def verify_otp(self, email: str, otp: str):
        """Verify the OTP and save the resulting token to credentials."""
        url = f"{self.base_url}/auth/cli/verify/"
        resp = self.session.post(url, json={"email": email, "otp": otp})
        if not resp.ok:
            raise APIError(resp.status_code, resp.text, response=resp)

        data = resp.json()
        token = data.get("token")
        if not token:
            raise APIError(
                resp.status_code, "No token returned from verification", response=resp
            )

        self._save_token(token)
        return token

    def _save_token(self, token: str):
        """Persist the token to ~/.bos/credentials."""
        creds_path = Path.home() / ".bos" / "credentials"
        creds_path.parent.mkdir(parents=True, exist_ok=True)
        creds_path.write_text(token.strip())
