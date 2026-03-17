from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.sql.task import Task
import uuid

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        """Create new task."""
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def delete(self, task: Task) -> None:
        """Delete existing task."""
        await self.session.delete(task)
        await self.session.commit()

    async def update(self, task: Task) -> Task:
        """Update existing task."""
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def get_task_by_id(self, task_id: uuid.UUID) -> Task | None:
        """Get task by it's ID."""
        statement = select(Task).where(Task.id == task_id)
        result = await self.session.execute(statement)
        return result.scalars().first()
    
    async def get_tasks_by_user(self, user_id: uuid.UUID) -> Task | None:
        """Get task by user ID."""
        statement = select(Task).where(Task.user_id == user_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())