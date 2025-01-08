from typing import List
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.run import Run


class RunsAPI(BaseAPI):
    """Async API endpoints related to Runs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def list_runs(self) -> List[Run]:
        resp = await self.get("/runs")
        return parse_obj_as(List[Run], resp)


class SyncRunsAPI(BaseAPI):
    """Synchronous API endpoints related to Runs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def list_runs(self) -> List[Run]:
        resp = self.get_sync("/runs")
        return parse_obj_as(List[Run], resp)
