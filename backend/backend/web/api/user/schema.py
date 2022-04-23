from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base class for User DTO model."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        allow_population_by_field_name = True


class UserCreate(UserBase):
    """DTO model for creating a new user."""

    username: str
    email: EmailStr
    hashed_password: str = Field(alias="password")


class UserUpdate(UserBase):
    """DTO model for updating an existing user."""

    hashed_password: Optional[str] = Field(None, alias="password")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None
    is_reported: Optional[bool] = None
    is_blocked: Optional[bool] = None
    preferences: Optional[str] = None
    updated_at: Optional[datetime] = None


class UserInDBBase(UserBase):
    """Base class for User from db DTO model."""

    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: bool
    is_active: bool
    is_reported: bool
    is_blocked: bool
    preferences: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """DTO model for User from db for output."""


class UserInDB(UserInDBBase):
    """DTO model for User from db."""

    hashed_password: str
