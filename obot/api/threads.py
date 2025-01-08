from typing import List, Dict
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.thread import Thread, ThreadMessage, ThreadCreateMessage


class ThreadsAPI(BaseAPI):
    """Async Threads API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def list_threads(self) -> List[Thread]:
        resp = await self.get("/threads")
        return parse_obj_as(List[Thread], resp)

    async def get_thread(self, thread_id: str) -> Thread:
        resp = await self.get(f"/threads/{thread_id}")
        return Thread(**resp)

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

    def list_threads(self) -> List[Thread]:
        resp = self.get_sync("/threads")
        return parse_obj_as(List[Thread], resp)

    def get_thread(self, thread_id: str) -> Thread:
        resp = self.get_sync(f"/threads/{thread_id}")
        return Thread(**resp)

    def delete_thread(self, thread_id: str) -> Dict[str, str]:
        return self.delete_sync(f"/threads/{thread_id}")

    def create_thread_message(
        self, thread_id: str, message_data: ThreadCreateMessage
    ) -> ThreadMessage:
        resp = self.post_sync(
            f"/threads/{thread_id}/messages", json=message_data.dict()
        )
        return ThreadMessage(**resp)
