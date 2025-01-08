"""
Synchronous ObotClient that composes resource-specific APIs.
"""

from typing import Optional
from urllib.parse import urljoin
from .api.agents import SyncAgentsAPI
from .api.workflows import SyncWorkflowsAPI
from .api.threads import SyncThreadsAPI
from .api.tools import SyncToolsAPI
from .api.models import SyncModelsAPI
from .api.credentials import SyncCredentialsAPI
from .api.webhooks import SyncWebhooksAPI


class ObotClient:
    """
    Synchronous client for the Obot API.
    """

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        """Initialize the client."""
        self._base_url = base_url.rstrip("/") + "/"
        self._token = token
        self._timeout = timeout

        # Initialize API clients
        self.agents = SyncAgentsAPI(base_url, token=token, timeout=timeout)
        self.workflows = SyncWorkflowsAPI(base_url, token=token, timeout=timeout)
        self.threads = SyncThreadsAPI(base_url, token=token, timeout=timeout)
        self.tools = SyncToolsAPI(base_url, token=token, timeout=timeout)
        self.models = SyncModelsAPI(base_url, token=token, timeout=timeout)
        self.credentials = SyncCredentialsAPI(base_url, token=token, timeout=timeout)
        self.webhooks = SyncWebhooksAPI(base_url, token=token, timeout=timeout)

    def close(self) -> None:
        """Close all underlying session clients."""
        self.agents.close_sync()
        self.workflows.close_sync()
        self.threads.close_sync()
        self.tools.close_sync()
        self.credentials.close_sync()
        self.webhooks.close_sync()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
