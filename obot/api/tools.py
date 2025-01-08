from typing import List, Dict, Any, Optional
from .base import BaseAPI
from ..models.tool import Tool


class ToolsAPI(BaseAPI):
    """Tools API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def __call__(self, category: Optional[str] = None) -> List[Tool]:
        """
        List all available tools (excluding model providers).

        Args:
            category: Optional category to filter tools by
        """
        resp = await self.get("/api/tool-references")
        tools = []

        for item in resp.get("items", []):
            # Only include items where toolType is "tool"
            if item.get("toolType") == "tool":
                # If category is specified, filter by it
                if category:
                    item_category = item.get("metadata", {}).get("category")
                    if item_category != category:
                        continue
                tools.append(Tool(**item))

        return tools

    async def categories(self) -> List[str]:
        """List all available tool categories."""
        resp = await self.get("/api/tool-references")
        categories = set()

        for item in resp.get("items", []):
            # Only include categories from actual tools
            if item.get("toolType") == "tool":
                category = item.get("metadata", {}).get("category")
                if category:
                    categories.add(category)

        return sorted(list(categories))


class SyncToolsAPI(BaseAPI):
    """Synchronous Tools API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def __call__(self, category: Optional[str] = None) -> List[Tool]:
        """
        List all available tools (excluding model providers).

        Args:
            category: Optional category to filter tools by
        """
        resp = self.get_sync("/api/tool-references")
        tools = []

        for item in resp.get("items", []):
            # Only include items where toolType is "tool"
            if item.get("toolType") == "tool":
                # If category is specified, filter by it
                if category:
                    item_category = item.get("metadata", {}).get("category")
                    if item_category != category:
                        continue
                tools.append(Tool(**item))

        return tools

    def categories(self) -> List[str]:
        """List all available tool categories."""
        resp = self.get_sync("/api/tool-references")
        categories = set()

        for item in resp.get("items", []):
            # Only include categories from actual tools
            if item.get("toolType") == "tool":
                category = item.get("metadata", {}).get("category")
                if category:
                    categories.add(category)

        return sorted(list(categories))
