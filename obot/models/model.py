from typing import Optional
from pydantic import BaseModel


class Model(BaseModel):
    """Model information."""

    id: str
    name: str
    type: str
    created: str
    revision: str
    targetModel: str
    modelProvider: str
    active: bool
    usage: str
    aliasAssigned: bool
