from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.db.dao.user import UserDAO
from backend.db.dependencies.user import get_current_user
from backend.db.models.user import User
from backend.exceptions import InvalidPasswordException, UserNotFoundException
from backend.security import create_access_token
from backend.web.api.auth.schema import Token
from backend.web.api.user import schema

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login_access_token(
    user_dao: UserDAO = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    """Returns access token if valid username and password are provided.

    Args:
        user_dao (UserDAO): User DAO.
        form_data (OAuth2PasswordRequestForm): User credentials.

    Raises:
        HTTPException: User not found or password is invalid.
        HTTPException: User is not active.
    """

    try:
        user = await user_dao.authenticate(form_data.username, form_data.password)
    except (UserNotFoundException, InvalidPasswordException) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    return {
        "access_token": create_access_token(str(user.id)),
        "token_type": "Bearer",
    }


@router.post("/test-token", response_model=schema.User)
async def token_test(
    current_user: User = Depends(get_current_user),
) -> User:
    """Returns current user if valid access token is provided

    Args:
        current_user (User): Current user.

    Returns:
        User: Current user.
    """

    return current_user
