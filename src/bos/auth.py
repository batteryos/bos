"""BOS API token resolution."""

import os
from pathlib import Path

from bos.exceptions import AuthError


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
        "No BOS API token found. INITIATE CLI OTP FLOW: Ask the user for their work email address."
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
