from typing import List, Optional
from .base import BaseAPI
from ..models.model_provider import ModelProvider
from ..models.model import Model


class ModelsAPI(BaseAPI):
    """Models API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def providers(self, configured: Optional[bool] = None) -> List[ModelProvider]:
        """
        List model providers with optional configuration filter.

        Args:
            configured: If True, only return configured providers.
                      If False, only return unconfigured providers.
                      If None, return all providers.
        """
        resp = await self.get("/api/model-providers")
        providers = [ModelProvider(**item) for item in resp.get("items", [])]

        if configured is not None:
            providers = [p for p in providers if p.configured == configured]

        return providers

    async def __call__(
        self, model_provider: Optional[str] = None, active: Optional[bool] = None
    ) -> List[Model]:
        """
        List all models with optional filters.

        Args:
            model_provider: Filter models by provider
            active: Filter models by active status
        """
        resp = await self.get("/api/models")
        models = [Model(**item) for item in resp.get("items", [])]

        if model_provider:
            models = [m for m in models if m.modelProvider == model_provider]

        if active is not None:
            models = [m for m in models if m.active == active]

        return models


class SyncModelsAPI(BaseAPI):
    """Synchronous Models API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def providers(self, configured: Optional[bool] = None) -> List[ModelProvider]:
        """
        List model providers with optional configuration filter.

        Args:
            configured: If True, only return configured providers.
                      If False, only return unconfigured providers.
                      If None, return all providers.
        """
        resp = self.get_sync("/api/model-providers")
        providers = [ModelProvider(**item) for item in resp.get("items", [])]

        if configured is not None:
            providers = [p for p in providers if p.configured == configured]

        return providers

    def __call__(
        self, model_provider: Optional[str] = None, active: Optional[bool] = None
    ) -> List[Model]:
        """
        List all models with optional filters.

        Args:
            model_provider: Filter models by provider
            active: Filter models by active status
        """
        resp = self.get_sync("/api/models")
        models = [Model(**item) for item in resp.get("items", [])]

        if model_provider:
            models = [m for m in models if m.modelProvider == model_provider]

        if active is not None:
            models = [m for m in models if m.active == active]

        return models
