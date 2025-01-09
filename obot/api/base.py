from typing import (
    Any,
    Dict,
    Optional,
    Union,
    List,
    TypeVar,
    Generic,
    Iterator,
    AsyncIterator,
    Tuple,
)
import httpx
import logging
from ..exceptions import (
    ObotAPIError,
    ObotAuthError,
    ObotConfigError,
    AgentNotFoundError,
)
from urllib.parse import urljoin
from httpx import HTTPStatusError

T = TypeVar("T")


class PaginatedResponse(Dict[str, Any]):
    """Helper class to handle paginated responses."""

    @property
    def items(self) -> List[Any]:
        return self.get("items", [])


class BaseAPI:
    """Base class for API endpoints."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: Optional[float] = None,
        is_async: bool = True,
        client: Optional["ObotClient"] = None,  # type: ignore
    ):
        """Initialize the API client."""
        self._base_url = base_url.rstrip("/") + "/"
        self._token = token
        self._timeout = timeout
        self._is_async = is_async
        self._client = client
        self._last_response_headers = {}

    def _get_headers(
        self, additional_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Get headers with authorization."""
        headers = {"Accept": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def _store_headers(self, headers: httpx.Headers) -> None:
        """Store response headers."""
        self._last_response_headers = dict(headers.items())

    def get_sync(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a synchronous GET request."""
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(
                urljoin(self._base_url, path.lstrip("/")),
                params=params,
                headers=self._get_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    def _handle_error(self, error: HTTPStatusError, context: str = "") -> None:
        """Handle HTTP errors and raise appropriate exceptions."""
        if error.response.status_code == 404 and "invoke" in str(error.request.url):
            agent_id = str(error.request.url).split("/")[-1]
            raise AgentNotFoundError(agent_id)

        message = f"API request failed: {context}" if context else "API request failed"
        raise ObotAPIError(
            message=message,
            status_code=error.response.status_code,
            response_text=error.response.text,
        )

    def post_sync(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make a synchronous POST request."""
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(
                    urljoin(self._base_url, path.lstrip("/")),
                    json=json,
                    data=data,
                    headers=self._get_headers(headers),
                )
                resp.raise_for_status()
                self._store_headers(resp.headers)
                return resp.text if data else resp.json()
        except httpx.HTTPStatusError as e:
            self._handle_error(e)
        except httpx.RequestError as e:
            raise ObotAPIError(f"Request failed: {str(e)}", status_code=0)

    def put_sync(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a synchronous PUT request."""
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.put(
                urljoin(self._base_url, path.lstrip("/")),
                json=json,
                data=data,
                headers=self._get_headers(headers),
            )
            resp.raise_for_status()
            return resp.json()

    def post_stream_sync(
        self,
        path: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Iterator[str]:
        """Make a synchronous streaming POST request."""
        with httpx.Client(timeout=self._timeout) as client:
            with client.stream(
                "POST",
                urljoin(self._base_url, path.lstrip("/")),
                data=data,
                headers=self._get_headers(headers),
            ) as resp:
                resp.raise_for_status()
                for chunk in resp.iter_text():
                    yield chunk

    async def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an asynchronous GET request."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.get(
                urljoin(self._base_url, path.lstrip("/")),
                params=params,
                headers=self._get_headers(),
            )
            resp.raise_for_status()
            return resp.json()

    async def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make an asynchronous POST request."""
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(
                    urljoin(self._base_url, path.lstrip("/")),
                    json=json,
                    data=data,
                    headers=self._get_headers(headers),
                )
                resp.raise_for_status()
                self._store_headers(resp.headers)
                return resp.text if data else resp.json()
        except httpx.HTTPStatusError as e:
            self._handle_error(e)
        except httpx.RequestError as e:
            raise ObotAPIError(f"Request failed: {str(e)}", status_code=0)

    async def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an asynchronous PUT request."""
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.put(
                urljoin(self._base_url, path.lstrip("/")),
                json=json,
                data=data,
                headers=self._get_headers(headers),
            )
            resp.raise_for_status()
            return resp.json()

    def post_stream(
        self,
        path: str,
        data: Optional[Union[str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncIterator[str]:
        """Make an asynchronous streaming POST request."""

        async def stream():
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream(
                    "POST",
                    urljoin(self._base_url, path.lstrip("/")),
                    data=data,
                    headers=self._get_headers(headers),
                ) as resp:
                    resp.raise_for_status()
                    self._store_headers(resp.headers)
                    async for chunk in resp.aiter_text():
                        yield chunk

        return stream()

    def close_sync(self) -> None:
        """Close the HTTP client session synchronously."""
        if self._is_async:
            raise RuntimeError("Cannot use sync methods on async client")
        self._client.close()

    async def close(self) -> None:
        """Close the HTTP client session asynchronously."""
        if not self._is_async:
            raise RuntimeError("Cannot use async methods on sync client")
        await self._client.aclose()

    def __enter__(self):
        if self._is_async:
            raise RuntimeError("Use async context manager for async client")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_sync()

    async def __aenter__(self):
        if not self._is_async:
            raise RuntimeError("Use sync context manager for sync client")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
