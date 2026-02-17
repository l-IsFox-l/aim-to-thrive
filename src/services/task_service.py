from fastapi import HTTPException
from src.models.pydantic.task import TaskCreate
from src.repositories.task import TaskRepository
from src.models.sql.task import Task, TaskType
import uuid


class TaskService:
    def __init__(self, task_repo:TaskRepository):
        self.task_repo = task_repo

    async def create_new_task(self, task_data: TaskCreate, user_id: uuid.UUID):
        """Create new task."""
        if task_data.task_type in [TaskType.NUMERIC, TaskType.DURATION]:
            if task_data.target_value is None or task_data.target_value <= 0:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Target value is required and must be > 0 for {task_data.task_type} tasks"
                )
            
        target_val = task_data.target_value
        if task_data.task_type == TaskType.BOOLEAN:
            target_val = 1.0
            
        new_task = Task(
            user_id = user_id,
            name = task_data.name,
            description = task_data.description,
            category = task_data.category,
            task_type = task_data.task_type,
            unit = task_data.unit,
            target_value = target_val,
            frequency_type = task_data.frequency_type,
            frequency_days = task_data.frequency_days
        )
        
        return await self.task_repo.create(new_task)