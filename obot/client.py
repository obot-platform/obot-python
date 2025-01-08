"""
Main AsyncObotClient that composes resource-specific APIs.
"""

from typing import Optional
from .api.agents import AgentsAPI
from .api.workflows import WorkflowsAPI
from .api.threads import ThreadsAPI
from .api.runs import RunsAPI
from .api.tools import ToolsAPI
from .api.credentials import CredentialsAPI
from .api.webhooks import WebhooksAPI


class AsyncObotClient:
    """
    High-level async client for accessing the Obot API.
    Composes multiple resource-specific APIs.
    """

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: float = 60.0,
    ):
        # Ensure base_url ends with /api
        if not base_url.endswith("/api"):
            base_url = f"{base_url.rstrip('/')}/api"

        self.agents = AgentsAPI(base_url, token=token, timeout=timeout)
        self.workflows = WorkflowsAPI(base_url, token=token, timeout=timeout)
        self.threads = ThreadsAPI(base_url, token=token, timeout=timeout)
        self.runs = RunsAPI(base_url, token=token, timeout=timeout)
        self.tools = ToolsAPI(base_url, token=token, timeout=timeout)
        self.credentials = CredentialsAPI(base_url, token=token, timeout=timeout)
        self.webhooks = WebhooksAPI(base_url, token=token, timeout=timeout)

    async def close(self) -> None:
        """Close all underlying session clients."""
        await self.agents.close()
        await self.workflows.close()
        await self.threads.close()
        await self.runs.close()
        await self.tools.close()
        await self.credentials.close()
        await self.webhooks.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
