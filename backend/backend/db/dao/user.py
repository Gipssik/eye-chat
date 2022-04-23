import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import ClauseElement

from backend.db.dependencies import get_db_session
from backend.db.models.user import User
from backend.exceptions import UserNotFoundException
from backend.security import hash_password, verify_password
from backend.web.api.user.schema import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserDAO:
    """Class for accessing user table"""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get(self, obj_id: str) -> User:
        db_obj = await self.session.get(User, obj_id)

        if not db_obj:
            logger.error(f"User {obj_id} not found")
            raise UserNotFoundException(f"User {obj_id} not found")

        logger.debug(f"Got user {db_obj.username}")
        return db_obj

    async def create(self, obj_in: UserCreate) -> User:
        obj_in.hashed_password, salt = hash_password(obj_in.hashed_password)
        obj_in_data = obj_in.dict()
        obj_in_data.update({"salt": salt})

        db_obj = User(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        logger.debug(f"Created user {db_obj.username}")
        return db_obj

    async def update(self, obj_in: UserUpdate, obj_id: str) -> User:
        db_obj = await self.get(obj_id)

        update_data = obj_in.dict(exclude_unset=True)
        if "hashed_password" in update_data:
            hashed_password, salt = hash_password(update_data["hashed_password"])
            update_data.update({"hashed_password": hashed_password, "salt": salt})

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        logger.debug(f"Updated user {db_obj.username}")
        return db_obj

    async def get_by_expr(self, expr: ClauseElement | list[ClauseElement]) -> User:
        if isinstance(expr, ClauseElement):
            expr = [expr]

        query = select(User).where(*expr)
        results = await self.session.execute(query)
        user = results.scalar()

        if not user:
            logger.error(f"User not found")
            raise UserNotFoundException(f"User not found")

        logger.debug(f"Got user {user.username}")
        return user

    async def authenticate(self, username: str, password: str) -> User:
        user = await self.get_by_expr(User.username == username)

        if not user:
            logger.error(f"User {username} not found")
            raise UserNotFoundException(f"User {username} not found")

        if not verify_password(password, user.salt, user.hashed_password):
            logger.error(f"User {username} password incorrect")
            raise UserNotFoundException(f"User {username} password incorrect")

        logger.debug(f"Authenticated user {username}")
        return user
