from passlib.context import CryptContext
from fastapi import HTTPException
from src.models.pydantic.user import UserCreate, UserRead
from src.repositories.user import UserRepository
from src.models.sql.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    async def register_new_user(self, user_data: UserCreate):
        # Check for existing user
        existing_user = await self.user_repo.get_by_email(user_data.email)
        existing_name = await self.user_repo.get_by_name(user_data.name)
        if existing_user or existing_name:
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed = pwd_context.hash(user_data.password)

        # Create models object
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed
        )

        # Save user
        return await self.user_repo.create(new_user)
    
    async def get_user_data(self, user_name: str):
        existing_user = await self.user_repo.get_by_name(user_name)
        if existing_user:
            return existing_user
        else:
            raise HTTPException(status_code=404, detail="User not found!")
        
    async def delete_user_by_name(self, user_name: str):
        user = await self.user_repo.get_by_name(user_name)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        await self.user_repo.delete(user)
        return {"status": "deleted" ,"message": f"User {user_name} deleted successfuly!"}
    
    async def update_username(self, user_name: str, new_name: str):
        user = await self.user_repo.get_by_name(user_name)
        if not user:
            raise HTTPException(status_code=400, detail="User not found!")
        
        existing_name = await self.user_repo.get_by_name(new_name)
        if existing_name:
            raise HTTPException(status_code=400, detail="You can't take already used name!")
        user.name = new_name
        await self.user_repo.update(user)
        return {"status": "updated", "message": f"User name({user_name}) updated to {new_name}!"}