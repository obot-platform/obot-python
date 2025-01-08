from typing import List
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.webhook import Webhook, WebhookCreate


class WebhooksAPI(BaseAPI):
    """Async API endpoints related to Webhooks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def list_webhooks(self) -> List[Webhook]:
        resp = await self.get("/webhooks")
        return parse_obj_as(List[Webhook], resp)

    async def create_webhook(self, webhook_data: WebhookCreate) -> Webhook:
        resp = await self.post("/webhooks", json=webhook_data.dict())
        return Webhook(**resp)

    async def delete_webhook(self, webhook_id: str) -> None:
        await self.delete(f"/webhooks/{webhook_id}")


class SyncWebhooksAPI(BaseAPI):
    """Synchronous API endpoints related to Webhooks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def list_webhooks(self) -> List[Webhook]:
        resp = self.get_sync("/webhooks")
        return parse_obj_as(List[Webhook], resp)

    def create_webhook(self, webhook_data: WebhookCreate) -> Webhook:
        resp = self.post_sync("/webhooks", json=webhook_data.dict())
        return Webhook(**resp)

    def delete_webhook(self, webhook_id: str) -> None:
        self.delete_sync(f"/webhooks/{webhook_id}")
