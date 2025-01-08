from typing import Optional
from pydantic import BaseModel


class Run(BaseModel):
    """Represents a run of something within the Obot system."""

    id: str
    status: str
    result: Optional[str] = None
