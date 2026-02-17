from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.sql.task import Task

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