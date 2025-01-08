from typing import Any, Dict, List
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.workflow import Workflow, WorkflowCreate


class WorkflowsAPI(BaseAPI):
    """Async Workflows API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def list_workflows(self) -> List[Workflow]:
        resp = await self.get("/workflows")
        return parse_obj_as(List[Workflow], resp)

    async def get_workflow(self, workflow_id: str) -> Workflow:
        resp = await self.get(f"/workflows/{workflow_id}")
        return Workflow(**resp)

    async def create_workflow(self, data: WorkflowCreate) -> Workflow:
        resp = await self.post("/workflows", json=data.dict())
        return Workflow(**resp)

    async def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return await self.delete(f"/workflows/{workflow_id}")


class SyncWorkflowsAPI(BaseAPI):
    """Synchronous Workflows API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def list_workflows(self) -> List[Workflow]:
        resp = self.get_sync("/workflows")
        return parse_obj_as(List[Workflow], resp)

    def get_workflow(self, workflow_id: str) -> Workflow:
        resp = self.get_sync(f"/workflows/{workflow_id}")
        return Workflow(**resp)

    def create_workflow(self, data: WorkflowCreate) -> Workflow:
        resp = self.post_sync("/workflows", json=data.dict())
        return Workflow(**resp)

    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self.delete_sync(f"/workflows/{workflow_id}")
