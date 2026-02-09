from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

# For circular imports issue
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
    timezone: str = Field(default="UTC")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Link to tasks
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})