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
from .api.chat import SyncChatAPI


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

        # Initialize API clients with self reference
        self.agents = SyncAgentsAPI(base_url, token=token, timeout=timeout, client=self)
        self.workflows = SyncWorkflowsAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.threads = SyncThreadsAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.tools = SyncToolsAPI(base_url, token=token, timeout=timeout, client=self)
        self.models = SyncModelsAPI(base_url, token=token, timeout=timeout, client=self)
        self.credentials = SyncCredentialsAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.webhooks = SyncWebhooksAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.chat = SyncChatAPI(base_url, token=token, timeout=timeout, client=self)

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
