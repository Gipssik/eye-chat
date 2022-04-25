import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.tests.utils import (
    create_random_user,
    create_user_with_exact_data,
    random_email,
)
from backend.web.api.auth.schema import Token


@pytest.mark.anyio
async def test_create_user_success(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_user")

    data = {
        "username": uuid.uuid4().hex,
        "email": random_email(),
        "password": uuid.uuid4().hex,
    }
    response = await client.post(
        url,
        json=data,
    )

    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert content["username"] == data["username"]
    assert content["email"] == data["email"]
    assert "hashed_password" not in content
    assert "first_name" in content
    assert "last_name" in content
    assert content["is_active"] is True
    assert content["is_reported"] is False
    assert content["is_blocked"] is False
    assert "preferences" in content
    assert "created_at" in content
    assert "updated_at" in content


@pytest.mark.anyio
async def test_create_user_fail_user_already_exists(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("create_user")

    user = await create_random_user(dbsession)
    data = {
        "username": user.username,
        "email": user.email,
        "password": uuid.uuid4().hex,
    }
    response = await client.post(
        url,
        json=data,
    )

    assert response.status_code == 409
    content = response.json()
    assert content["detail"] == "Username or email already exists"


@pytest.mark.anyio
async def test_get_user_success(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user = await create_random_user(dbsession)
    url = fastapi_app.url_path_for("get_user", user_id=str(user.id))

    response = await client.get(url)

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(user.id)
    assert content["username"] == user.username
    assert content["email"] == user.email
    assert "hashed_password" not in content
    assert content["first_name"] == user.first_name
    assert content["last_name"] == user.last_name
    assert content["is_active"] == user.is_active
    assert content["is_reported"] == user.is_reported
    assert content["is_blocked"] == user.is_blocked
    assert content["preferences"] == user.preferences
    assert "created_at" in content
    assert "updated_at" in content


@pytest.mark.anyio
async def test_get_user_fail_user_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_user", user_id=str(uuid.uuid4()))

    response = await client.get(url)

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "User not found"


@pytest.mark.anyio
async def test_update_user_success(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user, d = await create_user_with_exact_data(dbsession)

    token_url = fastapi_app.url_path_for("login_access_token")
    response = await client.post(
        token_url,
        data={"username": d["username"], "password": d["password"]},
    )
    token = Token(**response.json())

    user_url = fastapi_app.url_path_for("update_user", user_id=str(user.id))
    data = {
        "username": uuid.uuid4().hex,
        "email": random_email(),
        "password": uuid.uuid4().hex,
        "first_name": uuid.uuid4().hex,
        "last_name": uuid.uuid4().hex,
        "is_active": False,
        "is_reported": True,
        "is_blocked": True,
        "preferences": uuid.uuid4().hex,
    }
    response = await client.patch(
        user_url,
        json=data,
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(user.id)
    assert content["username"] == data["username"]
    assert content["email"] == data["email"]
    assert "hashed_password" not in content
    assert content["first_name"] == user.first_name
    assert content["last_name"] == user.last_name
    assert content["is_active"] == user.is_active
    assert content["is_reported"] == user.is_reported
    assert content["is_blocked"] == user.is_blocked
    assert content["preferences"] == user.preferences
    assert "created_at" in content
    assert content["updated_at"] != user.updated_at


@pytest.mark.anyio
async def test_update_user_fail_user_data_already_exists(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user = await create_random_user(dbsession)
    user2, d = await create_user_with_exact_data(dbsession)

    token_url = fastapi_app.url_path_for("login_access_token")
    response = await client.post(
        token_url,
        data={"username": d["username"], "password": d["password"]},
    )
    token = Token(**response.json())

    user2_url = fastapi_app.url_path_for("update_user", user_id=str(user2.id))
    data = {
        "username": user.username,
        "email": user.email,
    }
    response = await client.patch(
        user2_url,
        json=data,
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 409
    content = response.json()
    assert content["detail"] == "Username or email already exists"


@pytest.mark.anyio
async def test_update_user_fail_credentials_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user = await create_random_user(dbsession)

    url = fastapi_app.url_path_for("update_user", user_id=str(user.id))
    data = {
        "username": uuid.uuid4().hex,
        "email": random_email(),
    }
    response = await client.patch(
        url,
        json=data,
        headers={"Authorization": f"Bearer {uuid.uuid4().hex}"},
    )

    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Could not validate credentials"


@pytest.mark.anyio
async def test_delete_user_success(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user, d = await create_user_with_exact_data(dbsession)

    token_url = fastapi_app.url_path_for("login_access_token")
    response = await client.post(
        token_url,
        data={"username": d["username"], "password": d["password"]},
    )
    token = Token(**response.json())

    user_delete_url = fastapi_app.url_path_for("delete_user", user_id=str(user.id))
    response = await client.delete(
        user_delete_url,
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )
    assert response.status_code == 204

    user_get_url = fastapi_app.url_path_for("get_user", user_id=str(user.id))
    response = await client.get(user_get_url)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "User not found"


@pytest.mark.anyio
async def test_delete_user_fail_credentials_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user = await create_random_user(dbsession)

    url = fastapi_app.url_path_for("delete_user", user_id=str(user.id))
    response = await client.delete(
        url,
        headers={"Authorization": f"Bearer {uuid.uuid4().hex}"},
    )

    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Could not validate credentials"


@pytest.mark.anyio
async def test_user_me_success_api(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    user, d = await create_user_with_exact_data(dbsession)

    token_url = fastapi_app.url_path_for("login_access_token")
    response = await client.post(
        token_url,
        data={"username": d["username"], "password": d["password"]},
    )
    token = Token(**response.json())

    user_me_url = fastapi_app.url_path_for("get_user_me")
    response = await client.get(
        user_me_url,
        headers={"Authorization": f"{token.token_type} {token.access_token}"},
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(user.id)
    assert content["username"] == user.username
    assert content["email"] == user.email
    assert content["first_name"] == user.first_name
    assert content["last_name"] == user.last_name
    assert content["is_active"] == user.is_active
    assert content["is_reported"] == user.is_reported
    assert content["is_blocked"] == user.is_blocked
    assert content["preferences"] == user.preferences
    assert "created_at" in content
    assert "updated_at" in content


@pytest.mark.anyio
async def test_user_me_fail_credentials_error(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    url = fastapi_app.url_path_for("get_user_me")
    response = await client.get(
        url,
        headers={"Authorization": f"Bearer {uuid.uuid4().hex}"},
    )

    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Could not validate credentials"
