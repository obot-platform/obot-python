from typing import Optional, Union, Iterator
from dataclasses import dataclass


@dataclass
class Conversation:
    """A conversation with an agent."""

    agent_id: str
    thread_id: str
    _client: "ObotClient"  # type: ignore # Forward reference
    last_response: str

    def chat(self, message: str, stream: bool = False) -> Union[str, Iterator[str]]:
        """
        Continue the conversation with a new message.

        Args:
            message: The message to send
            stream: Whether to stream the response

        Returns:
            The agent's response
        """
        response = self._client.chat(
            self.agent_id, message, thread_id=self.thread_id, stream=stream
        )
        if not stream:
            self.last_response = response
        return response

    def __str__(self) -> str:
        """Return the last response when converting to string."""
        return self.last_response
