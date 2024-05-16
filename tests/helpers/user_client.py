import httpx


class UserClient:
    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url)

    async def healthz(self) -> httpx.Response:
        return await self._client.get("/healthz")

    async def create(self, body: dict[str, object]) -> httpx.Response:
        return await self._client.post("/", json=body)

    async def delete(self, user_id: str) -> httpx.Response:
        return await self._client.delete(f"/{user_id}")

    async def close(self) -> None:
        await self._client.aclose()
