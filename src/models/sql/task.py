from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

# For circular imports issue
if TYPE_CHECKING:
    from src.models.sql.user import User
    from src.models.sql.task_logs import TaskLogs

class TaskType(str, Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    DURATION = "duration"


class FrequencyType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"


class Task(SQLModel, table=True):
    """
    Represents a task.
    """
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True) # foreign key

    name: str = Field(index=True)
    description: str | None = None
    category: str = Field(index=True)
    task_type: TaskType

    # For numeric and duration
    unit: str | None = Field(default=None)
    target_value: float | None = Field(default=None)

    frequency_type: FrequencyType = FrequencyType.DAILY
    frequency_days: dict = Field(default_factory=dict ,sa_column=Column(JSONB, nullable=False))
    frequency_count: int | None = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: User = Relationship(back_populates="tasks")
    logs: List["TaskLogs"] = Relationship(back_populates="task", sa_relationship_kwargs={"cascade": "all, delete"})