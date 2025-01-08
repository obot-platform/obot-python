from typing import Any, Dict, Optional, Union, List, TypeVar, Generic
import httpx
import logging
from ..exceptions import ObotAPIError, ObotAuthError, ObotConfigError

T = TypeVar("T")


class PaginatedResponse(Dict[str, Any]):
    """Helper class to handle paginated responses."""

    @property
    def items(self) -> List[Any]:
        return self.get("items", [])


class BaseAPI:
    """Base class for making HTTP requests to the Obot API."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: float = 60.0,
        is_async: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.is_async = is_async

        # Initialize headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        # Create appropriate client based on sync/async mode
        if is_async:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=timeout,
            )
        else:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=timeout,
            )

    def _handle_response_sync(self, response: httpx.Response) -> Any:
        """Handle API response synchronously."""

        try:
            response_json = response.json()
        except Exception as e:
            response_json = None

        if not response.is_success:
            error_detail = (
                response_json.get("error") if response_json else response.text
            )

            if response.status_code == 401:
                raise ObotAuthError("Authentication failed")
            elif response.status_code == 403:
                raise ObotAuthError("Permission denied")
            else:
                raise ObotAPIError(
                    message=f"HTTP {response.status_code} Error: {error_detail}",
                    status_code=response.status_code,
                    response_data=response_json,
                )

        # Handle empty responses
        if response_json is None:
            if response.status_code == 204:  # No Content
                return []
            return {}

        # If the response is a dict with a data field, return the data
        if isinstance(response_json, dict) and "data" in response_json:
            return response_json["data"]

        return response_json

    async def _handle_response_async(self, response: httpx.Response) -> Any:
        """Handle API response asynchronously."""
        return self._handle_response_sync(response)

    # Sync methods
    def get_sync(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a synchronous GET request."""
        if self.is_async:
            raise RuntimeError("Cannot use sync methods on async client")

        full_url = f"{self.base_url}{path}"

        response = self._client.get(path, params=params)
        return self._handle_response_sync(response)

    def post_sync(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send POST request synchronously."""
        if self.is_async:
            raise RuntimeError("Cannot use sync methods on async client")
        response = self._client.post(path, json=json)
        return self._handle_response_sync(response)

    def put_sync(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send PUT request synchronously."""
        if self.is_async:
            raise RuntimeError("Cannot use sync methods on async client")
        response = self._client.put(path, json=json)
        return self._handle_response_sync(response)

    def delete_sync(self, path: str) -> Any:
        """Send DELETE request synchronously."""
        if self.is_async:
            raise RuntimeError("Cannot use sync methods on async client")
        response = self._client.delete(path)
        return self._handle_response_sync(response)

    # Async methods
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send GET request asynchronously."""
        if not self.is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        response = await self._client.get(path, params=params)
        return await self._handle_response_async(response)

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send POST request asynchronously."""
        if not self.is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        response = await self._client.post(path, json=json)
        return await self._handle_response_async(response)

    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send PUT request asynchronously."""
        if not self.is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        response = await self._client.put(path, json=json)
        return await self._handle_response_async(response)

    async def delete(self, path: str) -> Any:
        """Send DELETE request asynchronously."""
        if not self.is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        response = await self._client.delete(path)
        return await self._handle_response_async(response)

    def close_sync(self) -> None:
        """Close the HTTP client session synchronously."""
        if self.is_async:
            raise RuntimeError("Cannot use sync methods on async client")
        self._client.close()

    async def close(self) -> None:
        """Close the HTTP client session asynchronously."""
        if not self.is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        await self._client.aclose()

    def __enter__(self):
        if self.is_async:
            raise RuntimeError("Use async context manager for async client")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_sync()

    async def __aenter__(self):
        if not self.is_async:
            raise RuntimeError("Use sync context manager for sync client")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
