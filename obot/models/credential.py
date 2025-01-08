from typing import Optional
from pydantic import BaseModel


class Credential(BaseModel):
    """Represents a stored credential."""

    id: str
    provider: str
    secret_name: Optional[str] = None


class CredentialCreate(BaseModel):
    """Data required to store a new credential."""

    provider: str
    secret_name: str
    secret_value: str
