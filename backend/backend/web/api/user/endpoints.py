from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from backend.db.dao.user import UserDAO
from backend.db.dependencies.user import get_current_active_user
from backend.db.models.user import User
from backend.exceptions import UserNotFoundException
from backend.web.api.user import schema

router = APIRouter()


@router.get("/", response_model=list[schema.User])
async def get_users(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    user_dao: UserDAO = Depends(),
) -> list[User]:
    """Get list of users.

    Args:
        skip (Optional[int], optional): Number of users to skip. Defaults to 0.
        limit (Optional[int], optional): Max amount of users to return. Defaults to 100.
        user_dao (UserDAO, optional): User DAO.

    Returns:
        list[User]: List of users.
    """

    return await user_dao.get_multi(offset=skip, limit=limit)


@router.get("/me", response_model=schema.User)
async def get_user_me(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user.

    Args:
        current_user (User, optional): Current user.

    Returns:
        User: Current user.
    """

    return current_user


@router.get("/{user_id}", response_model=schema.User)
async def get_user(user_id: UUID, user_dao: UserDAO = Depends()) -> User:
    """Get user by id.

    Args:
        user_id (UUID): User ID.
        user_dao (UserDAO, optional): User DAO.

    Raises:
        UserNotFoundException: User not found.

    Returns:
        User: User.
    """

    try:
        return await user_dao.get(str(user_id))
    except UserNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from error


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user(user: schema.UserCreate, user_dao: UserDAO = Depends()) -> User:
    """Create new user.

    Args:
        user (schema.UserCreate): User data.
        user_dao (UserDAO, optional): User DAO.

    Raises:
        HTTPException: User already exists.

    Returns:
        User: User.
    """

    try:
        return await user_dao.create(user.dict())
    except IntegrityError as error:
        if "duplicate key" in str(error.__cause__):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists",
            )
        raise error


@router.patch("/{user_id}", response_model=schema.User)
async def update_user(
    user_id: UUID,
    user: schema.UserUpdate,
    user_dao: UserDAO = Depends(),
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Update user.

    Args:
        user_id (UUID): User ID.
        user (schema.UserUpdate): User data.
        user_dao (UserDAO, optional): User DAO.
        current_user (User, optional): Current user.

    Raises:
        HTTPException: You are not allowed to update this user.
        HTTPException: User not found.
        HTTPException: Username or email already exists.

    Returns:
        User: User.
    """

    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this user",
        )

    try:
        return await user_dao.update(user.dict(exclude_unset=True), str(user_id))
    except UserNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from error
    except IntegrityError as error:
        if "duplicate key" in str(error.__cause__):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists",
            )
        raise error


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_dao: UserDAO = Depends(),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Delete user.

    Args:
        user_id (UUID): User ID.
        user_dao (UserDAO, optional): User DAO.
        current_user (User, optional): Current user.

    Raises:
        HTTPException: You are not allowed to delete this user.
        HTTPException: User not found.
    """

    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this user",
        )

    try:
        await user_dao.delete(str(user_id))
    except UserNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from error
