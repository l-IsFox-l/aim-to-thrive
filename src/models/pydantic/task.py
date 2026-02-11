from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from src.models.sql.task import TaskType, FrequencyType

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    task_type: TaskType
    unit: Optional[str] = None
    target_value: Optional[float] = None
    frequency_type: FrequencyType
    frequency_days: Dict
    frequency_count: Optional[int] = None