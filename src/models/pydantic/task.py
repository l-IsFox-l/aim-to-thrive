from pydantic import BaseModel, Field
from typing import Optional, Dict
from src.models.sql.task import TaskType, FrequencyType
import uuid
import datetime

class TaskCreate(BaseModel):
    user_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field (..., min_length=1, max_length=100)
    task_type: TaskType
    unit: Optional[str] = None
    target_value: Optional[float] = None
    frequency_type: FrequencyType = FrequencyType.DAILY
    frequency_days: Dict = Field(default_factory=dict)

class TaskRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    category: str
    task_type: TaskType
    unit: Optional[str]
    target_value: Optional[float]
    frequency_type: FrequencyType
    frequency_days: Dict
    created_at: datetime.datetime
    updated_at: datetime.datetime

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    unit: Optional[str] = None
    target_value: Optional[float] = None
    