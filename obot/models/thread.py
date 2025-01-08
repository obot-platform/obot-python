from typing import Optional
from pydantic import BaseModel, Field


class Thread(BaseModel):
    """Represents a conversation thread."""

    id: str
    title: Optional[str] = None


class ThreadMessage(BaseModel):
    """Represents a single message in a thread."""

    id: str
    role: str
    content: str


class ThreadCreateMessage(BaseModel):
    """Data required to create a new message in a thread."""

    role: str = Field(..., description="System / user / assistant, etc.")
    content: str
