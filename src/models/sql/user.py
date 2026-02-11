from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from src.models.sql.task import Task

class User(SQLModel, table=True):
    """
    Represents a user in the multi-tenant system.
    """
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True ,index=True)
    hashed_password: str
    timezone: str = Field(default="UTC")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)