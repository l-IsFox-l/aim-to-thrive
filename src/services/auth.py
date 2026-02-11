from passlib.context import CryptContext
from fastapi import HTTPException
from src.models.pydantic.user import UserCreate
from src.repositories.user import UserRepository
from src.models.sql.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo:UserRepository):
        self.user_repo = user_repo

    async def register_new_user(self, user_data: UserCreate):
        # Check for existing user
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
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