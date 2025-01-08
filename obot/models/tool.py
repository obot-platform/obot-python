from typing import Dict, List, Optional
from pydantic import BaseModel


class Tool(BaseModel):
    """Tool model representing a tool reference."""

    id: str
    name: str
    description: str
    type: str
    toolType: str
    reference: str
    active: bool
    resolved: bool
    builtin: bool
    created: str
    revision: str
    credential: Optional[List[str]] = None
    params: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, str]] = None
    error: Optional[str] = None
