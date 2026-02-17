from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.sql.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalars().first()
    
    async def get_by_name(self, name: str) -> User | None:
        statement = select(User).where(User.name == name)
        result = await self.session.execute(statement)
        return result.scalars().first()
        
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def update(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user