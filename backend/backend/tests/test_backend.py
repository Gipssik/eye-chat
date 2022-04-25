import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """Checks the health endpoint.

    Args:
        client (AsyncClient): The client to use for the request.
        fastapi_app (FastAPI): The FastAPI application to use for the request.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
