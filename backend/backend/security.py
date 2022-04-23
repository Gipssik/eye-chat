import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from backend.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    user_id: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Creates an access token.

    Args:
        user_id (str): The user ID.
        expires_delta (timedelta, optional): Time delta for token expiration. Defaults to None.

    Returns:
        str: The access token.
    """

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes,
        )

    to_encode = {"exp": expire, "sub": user_id}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.encryption_algorithm,
    )
    return encoded_jwt


def hash_password(password: str) -> tuple[str, str]:
    """Returns a hashed version of the password.

    Args:
        password (str): The password to hash.

    Returns:
        tuple[str, str]: A tuple containing the hashed password and the salt.
    """

    salt = secrets.token_urlsafe(64)
    return pwd_context.hash(password + salt), salt


def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
    """Returns True if the password matches the hash.

    Args:
        plain_password (str): The password to check.
        salt (str): The salt used to hash the password.
        hashed_password (str): The hashed password to check against.

    Returns:
        bool: True if the password matches the hash.
    """

    return pwd_context.verify(plain_password + salt, hashed_password)
