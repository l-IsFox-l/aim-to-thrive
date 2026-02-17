from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.session import get_db
from src.repositories.task import TaskRepository
from src.services.task_service import TaskService
from src.models.pydantic.task import TaskCreate, TaskRead
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