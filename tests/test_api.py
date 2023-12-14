import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_currencies(fastapi_client: AsyncClient):
    response = await fastapi_client.get("/currencies")
    assert response.status_code == 200
