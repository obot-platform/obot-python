from typing import Optional
from pydantic import BaseModel


class Webhook(BaseModel):
    """Represents a webhook registered for certain events."""

    id: str
    url: str
    event: str


class WebhookCreate(BaseModel):
    """Data required to create a webhook."""

    url: str
    event: str
