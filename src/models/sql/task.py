import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.sql.base import Base

class TaskType(str, Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    DURATION = "duration"

class FrequencyType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)

    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    category: Mapped[str] = mapped_column(String(100), index=True)
    task_type: Mapped[TaskType] = mapped_column(String)

    unit: Mapped[Optional[str]] = mapped_column(String)
    target_value: Mapped[Optional[float]] = mapped_column(Float)

    frequency_type: Mapped[FrequencyType] = mapped_column(String, default=FrequencyType.DAILY)
    frequency_days: Mapped[dict] = mapped_column(JSON, default=dict)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="tasks")
    logs: Mapped[List["TaskLogs"]] = relationship(back_populates="task", cascade="all, delete-orphan")