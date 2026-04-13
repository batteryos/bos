"""BOS API exception hierarchy."""


class BOSError(Exception):
    """Base exception for all BOS errors."""


class AuthError(BOSError):
    """Token missing or invalid."""

    def __init__(
        self,
        message="No BOS API token found. Please use BOSAuth to complete the OTP verification flow.",
    ):
        super().__init__(message)


class APIError(BOSError):
    """Non-2xx response from the API."""

    def __init__(self, status_code, message=None, response=None):
        self.status_code = status_code
        if message is None:
            if status_code == 403:
                message = "Access forbidden. This may be due to an invalid token or insufficient permissions."
            elif status_code == 401:
                message = "Authentication failed. Your token may have expired."
            else:
                message = f"API request failed with status {status_code}"
        self.message = message
        self.response = response
        super().__init__(self.message)


class NotFoundError(APIError):
    """404 response."""

    def __init__(self, message=None, response=None):
        super().__init__(404, message or "Resource not found", response)
