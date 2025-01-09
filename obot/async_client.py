from typing import Optional
from urllib.parse import urljoin
from .api.agents import AgentsAPI
from .api.workflows import WorkflowsAPI
from .api.threads import ThreadsAPI
from .api.tools import ToolsAPI
from .api.models import ModelsAPI
from .api.credentials import CredentialsAPI
from .api.webhooks import WebhooksAPI
from .api.chat import ChatAPI


class AsyncObotClient:
    """Asynchronous client for the Obot API."""

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
        self.agents = AgentsAPI(base_url, token=token, timeout=timeout, client=self)
        self.workflows = WorkflowsAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.threads = ThreadsAPI(base_url, token=token, timeout=timeout, client=self)
        self.tools = ToolsAPI(base_url, token=token, timeout=timeout, client=self)
        self.models = ModelsAPI(base_url, token=token, timeout=timeout, client=self)
        self.credentials = CredentialsAPI(
            base_url, token=token, timeout=timeout, client=self
        )
        self.webhooks = WebhooksAPI(base_url, token=token, timeout=timeout, client=self)
        self.chat = ChatAPI(base_url, token=token, timeout=timeout, client=self)
