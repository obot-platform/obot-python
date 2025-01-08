from typing import List, Optional
from pydantic import BaseModel


class ModelProvider(BaseModel):
    """Model provider information."""

    id: str
    name: str
    type: str
    created: str
    revision: str
    icon: str
    toolReference: str
    configured: bool
    requiredConfigurationParameters: List[str]
    missingConfigurationParameters: Optional[List[str]] = None
    optionalConfigurationParameters: Optional[List[str]] = None
    modelsBackPopulated: Optional[bool] = None
