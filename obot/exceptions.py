from typing import Any, Optional


class ObotError(Exception):
    """Base exception for all Obot-related errors."""

    pass


class ObotAPIError(ObotError):
    """Raised when the Obot API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class ObotAuthError(ObotError):
    """Raised when there are authentication/authorization issues."""

    pass


class ObotConfigError(ObotError):
    """Raised when there are configuration issues."""

    pass
