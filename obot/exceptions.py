from typing import Any, Optional
from httpx import HTTPStatusError


class ObotError(Exception):
    """Base exception for all Obot errors."""

    pass


class AgentNotFoundError(ObotError):
    """Raised when an agent is not found."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        super().__init__(f"Agent '{agent_id}' not found")


class ObotAPIError(ObotError):
    """Raised when the API returns an error."""

    def __init__(
        self, message: str, status_code: int, response_text: Optional[str] = None
    ):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"{message} (Status: {status_code})")


class ObotAuthError(ObotError):
    """Raised when there are authentication/authorization issues."""

    pass


class ObotConfigError(ObotError):
    """Raised when there are configuration issues."""

    pass
