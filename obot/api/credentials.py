from typing import List, Dict
from pydantic import parse_obj_as
from .base import BaseAPI
from ..models.credential import Credential, CredentialCreate


class CredentialsAPI(BaseAPI):
    """Async API endpoints related to Credentials."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=True, **kwargs)

    async def list_credentials(self) -> List[Credential]:
        resp = await self.get("/credentials")
        return parse_obj_as(List[Credential], resp)

    async def create_credential(self, cred_data: CredentialCreate) -> Credential:
        resp = await self.post("/credentials", json=cred_data.dict())
        return Credential(**resp)

    async def delete_credential(self, credential_id: str) -> Dict[str, str]:
        return await self.delete(f"/credentials/{credential_id}")


class SyncCredentialsAPI(BaseAPI):
    """Synchronous API endpoints related to Credentials."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, is_async=False, **kwargs)

    def list_credentials(self) -> List[Credential]:
        resp = self.get_sync("/credentials")
        return parse_obj_as(List[Credential], resp)

    def create_credential(self, cred_data: CredentialCreate) -> Credential:
        resp = self.post_sync("/credentials", json=cred_data.dict())
        return Credential(**resp)

    def delete_credential(self, credential_id: str) -> Dict[str, str]:
        return self.delete_sync(f"/credentials/{credential_id}")
