import uuid

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dao.user import UserDAO
from backend.db.models.user import User
from backend.web.api.user import schema


def random_email() -> str:
    fake = Faker()
    return fake.free_email()


async def create_random_user(dbsession: AsyncSession) -> User:
    data = {
        "username": uuid.uuid4().hex,
        "email": random_email(),
        "password": uuid.uuid4().hex,
    }
    user = schema.UserCreate(**data)

    user_dao = UserDAO(dbsession)
    return await user_dao.create(user.dict())


async def create_user_with_exact_data(
    dbsession: AsyncSession,
) -> tuple[User, dict[str, str]]:
    data = {
        "username": "test_user",
        "email": random_email(),
        "password": "test_password",
    }
    user = schema.UserCreate(**data)

    user_dao = UserDAO(dbsession)
    return await user_dao.create(user.dict()), data
