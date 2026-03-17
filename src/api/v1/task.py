from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.session import get_db
from src.repositories.task import TaskRepository
from src.services.task_service import TaskService
from src.models.pydantic.task import TaskCreate, TaskRead, TaskUpdate
import uuid

router = APIRouter()

@router.post("/create_task", response_model=TaskRead)
async def create_task(
    task_data: TaskCreate,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Create task."""
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.create_new_task(task_data, user_id)

@router.get("/get_task_by_id")
async def get_task_by_id(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get task by it's ID."""
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.get_task_by_id(task_id)

@router.get("/get_task_by_user")
async def get_tasks_by_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get tasks by user's ID."""
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.get_all_tasks_by_user(user_id)

@router.put("/update_task")
async def update_task(
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update existing task."""
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)
    
    return await service.update_task_data(user_id, task_id, task_data)

@router.delete("/delete_task")
async def delete_task(
    task_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete existing task."""
    task_repo = TaskRepository(db)
    service = TaskService(task_repo)

    return await service.delete_task(user_id, task_id)