from typing import Optional, AsyncIterator, Iterator, List, Dict
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.thread import Thread, ThreadMessage, ThreadCreateMessage


class ThreadsAPI(BaseAPI):
    """Async Threads API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def __call__(self) -> List[Thread]:
        """List all threads."""
        resp = await self.get("/api/threads")
        return [Thread(**item) for item in resp.get("items", [])]

    async def get(self, thread_id: str) -> Thread:
        """Get a specific thread."""
        resp = await self.get(f"/api/threads/{thread_id}")
        return Thread(**resp)

    async def chat(
        self,
        agent_id: str,
        message: str,
        thread_id: Optional[str] = None,
        stream: bool = True,
    ) -> AsyncIterator[str]:
        """
        Send a message to an agent and get the response.

        Args:
            agent_id: The ID of the agent to chat with
            message: The message to send
            thread_id: Optional thread ID to continue a conversation
            stream: Whether to stream the response (default: True)

        Yields:
            Response chunks from the agent
        """
        headers = {"Content-Type": "text/plain"}
        if thread_id:
            headers["X-Obot-Thread-Id"] = thread_id

        async with self.stream(
            "POST", f"/api/invoke/{agent_id}", content=message, headers=headers
        ) as response:
            thread_id = response.headers.get("X-Obot-Thread-Id")
            async for chunk in response.aiter_text():
                yield chunk

    async def delete_thread(self, thread_id: str) -> Dict[str, str]:
        return await self.delete(f"/threads/{thread_id}")

    async def create_thread_message(
        self, thread_id: str, message_data: ThreadCreateMessage
    ) -> ThreadMessage:
        resp = await self.post(
            f"/threads/{thread_id}/messages", json=message_data.dict()
        )
        return ThreadMessage(**resp)


class SyncThreadsAPI(BaseAPI):
    """Synchronous Threads API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def __call__(self) -> List[Thread]:
        """List all threads."""
        resp = self.get_sync("/api/threads")
        return [Thread(**item) for item in resp.get("items", [])]

    def get(self, thread_id: str) -> Thread:
        """Get a specific thread."""
        resp = self.get_sync(f"/api/threads/{thread_id}")
        return Thread(**resp)

    def chat(
        self,
        agent_id: str,
        message: str,
        thread_id: Optional[str] = None,
        stream: bool = True,
    ) -> Iterator[str]:
        """
        Send a message to an agent and get the response.

        Args:
            agent_id: The ID of the agent to chat with
            message: The message to send
            thread_id: Optional thread ID to continue a conversation
            stream: Whether to stream the response (default: True)

        Yields:
            Response chunks from the agent
        """
        headers = {"Content-Type": "text/plain"}
        if thread_id:
            headers["X-Obot-Thread-Id"] = thread_id

        with self.stream_sync(
            "POST", f"/api/invoke/{agent_id}", content=message, headers=headers
        ) as response:
            thread_id = response.headers.get("X-Obot-Thread-Id")
            for chunk in response.iter_text():
                yield chunk

    def delete_thread(self, thread_id: str) -> Dict[str, str]:
        return self.delete_sync(f"/threads/{thread_id}")

    def create_thread_message(
        self, thread_id: str, message_data: ThreadCreateMessage
    ) -> ThreadMessage:
        resp = self.post_sync(
            f"/threads/{thread_id}/messages", json=message_data.dict()
        )
        return ThreadMessage(**resp)
