from typing import Optional
from pydantic import BaseModel, Field


class Workflow(BaseModel):
    """Represents an existing workflow."""

    id: str
    name: str
    description: Optional[str] = None


class WorkflowCreate(BaseModel):
    """Data required to create a workflow."""

    name: str = Field(..., description="Name of the workflow")
    description: Optional[str] = Field(None, description="Description of the workflow")
