from typing import Optional, Union, Iterator, AsyncIterator
from dataclasses import dataclass


@dataclass
class Conversation:
    """A conversation with an agent."""

    agent_id: str
    thread_id: str
    _client: Union["ObotClient", "AsyncObotClient"]  # type: ignore
    last_response: str

    async def achat(
        self, message: str, stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        """
        Continue the conversation with a new message (async version).

        Args:
            message: The message to send
            stream: Whether to stream the response

        Returns:
            The agent's response
        """
        if not hasattr(self._client.chat, "__call__"):
            raise RuntimeError("Async chat not available")

        response = await self._client.chat(
            self.agent_id, message, thread_id=self.thread_id, stream=stream
        )

        if not stream:
            self.last_response = response
            return response

        # For streaming responses, we need to await the async iterator
        return response

    def chat(self, message: str, stream: bool = False) -> Union[str, Iterator[str]]:
        """
        Continue the conversation with a new message (sync version).

        Args:
            message: The message to send
            stream: Whether to stream the response

        Returns:
            The agent's response
        """
        if not hasattr(self._client.chat, "__call__"):
            raise RuntimeError("Sync chat not available")

        response = self._client.chat(
            self.agent_id, message, thread_id=self.thread_id, stream=stream
        )

        if not stream:
            self.last_response = response
        return response

    def __str__(self) -> str:
        """Return the last response when converting to string."""
        return self.last_response
