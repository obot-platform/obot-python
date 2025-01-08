from typing import List, Optional, Dict, Any, Union
from httpx import Response
from .base import BaseAPI
from ..models import Agent, Model, Tool


class AgentsAPI(BaseAPI):
    """
    Async Agents API endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def __call__(self) -> List[Agent]:
        """List all agents."""
        resp = await self.get("/api/agents")
        return [Agent(**item) for item in resp.get("items", [])]

    async def get(self, agent_id: str) -> Agent:
        """
        Get a specific agent by ID.

        Args:
            agent_id: The ID of the agent to retrieve
        """
        resp = await self.get(f"/api/agents/{agent_id}")
        return Agent(**resp)

    async def _get_model_id(self, model_name: str) -> str:
        """
        Convert a model name to its ID.

        Args:
            model_name: The name of the model to look up

        Raises:
            ValueError: If the model name doesn't exist or isn't active
        """
        resp = await self.get("/api/models")
        models = [Model(**item) for item in resp.get("items", [])]
        active_models = [m for m in models if m.active]

        for model in active_models:
            if model.name == model_name:
                return model.id

        raise ValueError(
            f"Model '{model_name}' not found or not active. Available active models: "
            f"{', '.join(m.name for m in active_models)}"
        )

    async def _get_tool_ids(self, tool_names: List[str]) -> List[str]:
        """
        Convert tool names to their IDs.

        Args:
            tool_names: List of tool names to convert

        Returns:
            List of tool IDs

        Raises:
            ValueError: If any tool name doesn't exist
        """
        resp = await self.get("/api/tool-references")
        tools = [
            Tool(**item)
            for item in resp.get("items", [])
            if item.get("toolType") == "tool"
        ]

        tool_map = {tool.name: tool.id for tool in tools}
        invalid_tools = [name for name in tool_names if name not in tool_map]

        if invalid_tools:
            raise ValueError(
                f"Invalid tool names: {', '.join(invalid_tools)}. "
                f"Available tools: {', '.join(tool_map.keys())}"
            )

        return [tool_map[name] for name in tool_names]

    async def _validate_tool_ids(self, tool_ids: List[str]) -> None:
        """
        Validate that the provided tool IDs exist.

        Args:
            tool_ids: List of tool IDs to validate

        Raises:
            ValueError: If any tool ID doesn't exist
        """
        resp = await self.get("/api/tool-references")
        tools = [
            Tool(**item)
            for item in resp.get("items", [])
            if item.get("toolType") == "tool"
        ]

        valid_ids = {tool.id for tool in tools}
        invalid_ids = [tid for tid in tool_ids if tid not in valid_ids]

        if invalid_ids:
            raise ValueError(
                f"Invalid tool IDs: {', '.join(invalid_ids)}. "
                f"Available tool IDs: {', '.join(valid_ids)}"
            )

    async def create(self, **kwargs) -> Agent:
        """
        Create a new agent.

        Args:
            name: Agent name
            description: Agent description
            prompt: Agent prompt
            model: Model name (will be converted to model ID)
            tools: List of tool IDs

        Raises:
            ValueError: If the model doesn't exist or any tool IDs are invalid
        """
        if "model" in kwargs:
            kwargs["model"] = await self._get_model_id(kwargs["model"])

        if "tools" in kwargs:
            await self._validate_tool_ids(kwargs["tools"])

        resp = await self.post("/api/agents", json=kwargs)
        return Agent(**resp)

    async def update(self, agent_id: str, **kwargs) -> Agent:
        """
        Update specific fields of an existing agent.

        Args:
            agent_id: The ID of the agent to update
            **kwargs: Fields to update (only specified fields will be modified), including:
                name: Agent name
                description: Agent description
                prompt: Agent prompt
                model: Model name (will be converted to model ID)
                tools: List of tool IDs

        Raises:
            ValueError: If the model doesn't exist or any tool IDs are invalid
        """
        # Get current agent state
        current_agent = await self.get(agent_id)
        update_data = current_agent.model_dump(exclude_unset=True)

        # Only update fields that were passed
        if "model" in kwargs:
            kwargs["model"] = await self._get_model_id(kwargs["model"])

        if "tools" in kwargs:
            await self._validate_tool_ids(kwargs["tools"])

        update_data.update(kwargs)
        resp = await self.put(f"/api/agents/{agent_id}", json=update_data)
        return Agent(**resp)


class SyncAgentsAPI(BaseAPI):
    """
    Synchronous Agents API endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def __call__(self) -> List[Agent]:
        """List all agents."""
        resp = self.get_sync("/api/agents")
        return [Agent(**item) for item in resp.get("items", [])]

    def get(self, agent_id: str) -> Agent:
        """
        Get a specific agent by ID.

        Args:
            agent_id: The ID of the agent to retrieve
        """
        resp = self.get_sync(f"/api/agents/{agent_id}")
        return Agent(**resp)

    def _get_model_id(self, model_name: str) -> str:
        """
        Convert a model name to its ID.

        Args:
            model_name: The name of the model to look up

        Raises:
            ValueError: If the model name doesn't exist or isn't active
        """
        resp = self.get_sync("/api/models")
        models = [Model(**item) for item in resp.get("items", [])]
        active_models = [m for m in models if m.active]

        for model in active_models:
            if model.name == model_name:
                return model.id

        raise ValueError(
            f"Model '{model_name}' not found or not active. Available active models: "
            f"{', '.join(m.name for m in active_models)}"
        )

    def _get_tool_ids(self, tool_names: List[str]) -> List[str]:
        """
        Convert tool names to their IDs.

        Args:
            tool_names: List of tool names to convert

        Returns:
            List of tool IDs

        Raises:
            ValueError: If any tool name doesn't exist
        """
        resp = self.get_sync("/api/tool-references")
        tools = [
            Tool(**item)
            for item in resp.get("items", [])
            if item.get("toolType") == "tool"
        ]

        tool_map = {tool.name: tool.id for tool in tools}
        invalid_tools = [name for name in tool_names if name not in tool_map]

        if invalid_tools:
            raise ValueError(
                f"Invalid tool names: {', '.join(invalid_tools)}. "
                f"Available tools: {', '.join(tool_map.keys())}"
            )

        return [tool_map[name] for name in tool_names]

    def _validate_tool_ids(self, tool_ids: List[str]) -> None:
        """
        Validate that the provided tool IDs exist.

        Args:
            tool_ids: List of tool IDs to validate

        Raises:
            ValueError: If any tool ID doesn't exist
        """
        resp = self.get_sync("/api/tool-references")
        tools = [
            Tool(**item)
            for item in resp.get("items", [])
            if item.get("toolType") == "tool"
        ]

        valid_ids = {tool.id for tool in tools}
        invalid_ids = [tid for tid in tool_ids if tid not in valid_ids]

        if invalid_ids:
            raise ValueError(
                f"Invalid tool IDs: {', '.join(invalid_ids)}. "
                f"Available tool IDs: {', '.join(valid_ids)}"
            )

    def create(self, **kwargs) -> Agent:
        """
        Create a new agent.

        Args:
            name: Agent name
            description: Agent description
            prompt: Agent prompt
            model: Model name (will be converted to model ID)
            tools: List of tool IDs

        Raises:
            ValueError: If the model doesn't exist or any tool IDs are invalid
        """
        if "model" in kwargs:
            kwargs["model"] = self._get_model_id(kwargs["model"])

        if "tools" in kwargs:
            self._validate_tool_ids(kwargs["tools"])

        resp = self.post_sync("/api/agents", json=kwargs)
        return Agent(**resp)

    def update(self, agent_id: str, **kwargs) -> Agent:
        """
        Update specific fields of an existing agent.

        Args:
            agent_id: The ID of the agent to update
            **kwargs: Fields to update (only specified fields will be modified), including:
                name: Agent name
                description: Agent description
                prompt: Agent prompt
                model: Model name (will be converted to model ID)
                tools: List of tool IDs

        Raises:
            ValueError: If the model doesn't exist or any tool IDs are invalid
        """
        # Get current agent state
        current_agent = self.get(agent_id)
        update_data = current_agent.model_dump(exclude_unset=True)

        # Only update fields that were passed
        if "model" in kwargs:
            kwargs["model"] = self._get_model_id(kwargs["model"])

        if "tools" in kwargs:
            self._validate_tool_ids(kwargs["tools"])

        update_data.update(kwargs)
        resp = self.put_sync(f"/api/agents/{agent_id}", json=update_data)
        return Agent(**resp)
