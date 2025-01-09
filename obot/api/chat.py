from typing import Optional, Union, Iterator, AsyncIterator
import json
from .base import BaseAPI
from ..models.conversation import Conversation


def _extract_message(response: str) -> str:
    """
    Extract the complete message from the response JSON.

    Args:
        response: JSON string containing the response items

    Returns:
        The complete message from the model
    """
    try:
        data = json.loads(response)
        message = ""

        # Combine all content chunks that aren't system messages
        for item in data.get("items", []):
            if "content" in item and "contentID" in item:
                message += item["content"]

        return message.strip()
    except json.JSONDecodeError:
        return response.strip()


class ChatAPI(BaseAPI):
    """Async Chat API endpoints."""

    async def __call__(
        self,
        agent_id: str,
        message: str,
        *,
        thread_id: Optional[str] = None,
        stream: bool = False,
        return_conversation: bool = True,
    ) -> Union[str, AsyncIterator[str], Conversation]:
        """
        Send a message to an agent and get the response.

        Args:
            agent_id: The ID of the agent to chat with
            message: The message to send
            thread_id: Optional thread ID to continue a conversation
            stream: Whether to stream the response
            return_conversation: Whether to return a Conversation object

        Returns:
            If return_conversation=True, returns a Conversation object
            If stream=True, returns an async iterator of response chunks
            Otherwise, returns the response as a string
        """
        headers = {
            "Content-Type": "text/plain",
        }

        if thread_id:
            headers["X-Obot-Thread-Id"] = thread_id

        if stream:
            return self.post_stream(
                f"/api/invoke/{agent_id}", data=message, headers=headers
            )

        resp = await self.post(f"/api/invoke/{agent_id}", data=message, headers=headers)
        response_text = _extract_message(resp)

        if return_conversation:
            # Get thread ID from response headers
            new_thread_id = thread_id or self._last_response_headers.get(
                "X-Obot-Thread-Id"
            )
            if not new_thread_id:
                raise ValueError("No thread ID found in response headers")

            return Conversation(
                agent_id=agent_id,
                thread_id=new_thread_id,
                _client=self._client,
                last_response=response_text,
            )

        return response_text


class SyncChatAPI(BaseAPI):
    """Synchronous Chat API endpoints."""

    def __call__(
        self,
        agent_id: str,
        message: str,
        *,
        thread_id: Optional[str] = None,
        stream: bool = False,
        return_conversation: bool = True,
    ) -> Union[str, Iterator[str], Conversation]:
        """
        Send a message to an agent and get the response.

        Args:
            agent_id: The ID of the agent to chat with
            message: The message to send
            thread_id: Optional thread ID to continue a conversation
            stream: Whether to stream the response
            return_conversation: Whether to return a Conversation object

        Returns:
            If return_conversation=True, returns a Conversation object
            If stream=True, returns an iterator of response chunks
            Otherwise, returns the response as a string
        """
        headers = {
            "Content-Type": "text/plain",
        }

        if thread_id:
            headers["X-Obot-Thread-Id"] = thread_id

        if stream:
            return self.post_stream_sync(
                f"/api/invoke/{agent_id}", data=message, headers=headers
            )

        resp = self.post_sync(f"/api/invoke/{agent_id}", data=message, headers=headers)
        response_text = _extract_message(resp)

        if return_conversation:
            # Get thread ID from response headers
            new_thread_id = thread_id or self._last_response_headers.get(
                "x-obot-thread-id"
            )
            if not new_thread_id:
                raise ValueError(
                    f"No thread ID found in response headers. Headers: {self._last_response_headers}"
                )

            return Conversation(
                agent_id=agent_id,
                thread_id=new_thread_id,
                _client=self._client,
                last_response=response_text,
            )

        return response_text
