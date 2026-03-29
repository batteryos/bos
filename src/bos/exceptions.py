"""BOS API exception hierarchy."""


class BOSError(Exception):
    """Base exception for all BOS errors."""


class AuthError(BOSError):
    """Token missing or invalid."""


class APIError(BOSError):
    """Non-2xx response from the API."""

    def __init__(self, status_code, message=None, response=None):
        self.status_code = status_code
        self.message = message or f"API request failed with status {status_code}"
        self.response = response
        super().__init__(self.message)


class NotFoundError(APIError):
    """404 response."""

    def __init__(self, message=None, response=None):
        super().__init__(404, message or "Resource not found", response)
