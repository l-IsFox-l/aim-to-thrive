from fastapi import HTTPException
from src.models.pydantic.task import TaskCreate, TaskUpdate
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
    
    async def get_all_tasks_by_user(self, user_id: uuid.UUID):
        """Get all task by the user ID."""
        users_tasks = await self.task_repo.get_tasks_by_user(user_id)
        if users_tasks:
            return users_tasks
        else:
            raise HTTPException(status_code=404, detail="Now task found for this user!")
        
    async def get_task_by_id(self, task_id: uuid.UUID):
        """Get task by ID."""
        task_by_id = await self.task_repo.get_task_by_id(task_id)
        if task_by_id:
            return task_by_id
        else:
            raise HTTPException(status_code=404, detail="Task with id: {task_id} not found!")
    
    async def update_task_data(self, user_id: uuid.UUID, task_id: uuid.UUID, update_data: TaskUpdate):
        """Update task data."""
        task = await self.task_repo.get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found!")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Premission denied!")
        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(task, key, value)

        return await self.task_repo.update(task)
    
    async def delete_task(self, user_id: uuid.UUID, task_id: uuid.UUID):
        """Delete existing task."""
        task = await self.task_repo.get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found!")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Premission denied!")
        await self.task_repo.delete(task)
        return {"status": "deleted" ,"message": f"Task '{task.name}' deleted successfuly!"}