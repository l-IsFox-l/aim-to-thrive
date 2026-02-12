import uuid
import datetime
from sqlalchemy import ForeignKey, Date, DateTime, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.sql.base import Base

class TaskLogs(Base):
    __tablename__ = "task_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"), index=True)
    
    date: Mapped[datetime.date] = mapped_column(Date, index=True)
    current_value: Mapped[float] = mapped_column(default=0.0)
    is_completed: Mapped[bool] = mapped_column(default=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    task: Mapped["Task"] = relationship(back_populates="logs")

    __table_args__ = (
        UniqueConstraint("task_id", "date", name="unique_task_log_per_day"),
    )