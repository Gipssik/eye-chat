import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = sa.Column(sa.String(32), nullable=False, unique=True, index=True)
    email = sa.Column(sa.String, nullable=False, unique=True, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    is_superuser = sa.Column(sa.Boolean, nullable=False, default=False)
    is_active = sa.Column(sa.Boolean, nullable=False, default=True)
    is_reported = sa.Column(sa.Boolean, nullable=False, default=False)
    is_blocked = sa.Column(sa.Boolean, nullable=False, default=False)
    preferences = sa.Column(sa.Text)
    created_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_at = sa.Column(
        sa.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    salt = sa.Column(sa.String, nullable=False)
