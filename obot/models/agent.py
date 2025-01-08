from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AgentLinks(BaseModel):
    invoke: str


class AgentIcons(BaseModel):
    icon: Optional[str] = None
    iconDark: Optional[str] = None
    collapsed: Optional[str] = None
    collapsedDark: Optional[str] = None


class Agent(BaseModel):
    """Represents an agent."""

    # Required fields for creation
    name: str

    # Optional fields for creation
    description: str = ""
    prompt: str = ""
    model: str = ""
    tools: Optional[List[str]] = None

    # Server-populated fields
    id: Optional[str] = None
    created: Optional[str] = None
    revision: Optional[str] = None
    links: Optional[AgentLinks] = None
    type: str = "agent"
    icons: Optional[AgentIcons] = None
    default: bool = False
    temperature: Optional[float] = None
    cache: Optional[Any] = None
    alias: str = ""
    knowledgeDescription: str = ""
    agents: Optional[List[str]] = None
    workflows: Optional[List[str]] = None
    availableThreadTools: Optional[List[str]] = None
    defaultThreadTools: Optional[List[str]] = None
    oauthApps: Optional[Any] = None
    maxThreadTools: int = 0
    params: Optional[Dict[str, Any]] = None
    env: Optional[Dict[str, str]] = None
    aliasAssigned: bool = False
    toolInfo: Optional[Dict[str, Dict[str, Any]]] = None


class AgentCreate(BaseModel):
    """Data required to create a new agent."""

    name: str = Field(..., description="Name of the agent")
    description: Optional[str] = Field("", description="Description of the agent")
    prompt: Optional[str] = Field("", description="Prompt context for the agent")
    model: Optional[str] = Field("", description="Model ID to use for the agent")
    tools: Optional[List[str]] = Field(None, description="List of tool IDs to enable")
