from __future__ import annotations
import uuid
from datetime import datetime, date
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship

if TYPE_CHECKING:
    from src.models.sql.task import Task

class TaskLogs(SQLModel, table=True):
    """ """
    __tablename__ = "task_logs"

    __table_args__ = (
        UniqueConstraint("task_id", "date", name="unique_task_log_per_day"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_id: uuid.UUID = Field(foreign_key="tasks.id", index=True) # Foreign key
    date: date = Field(index=True)
    current_value: float = Field(default=0.0)
    is_completed: bool = Field(default=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    task: "Task" = Relationship(back_populates="logs")