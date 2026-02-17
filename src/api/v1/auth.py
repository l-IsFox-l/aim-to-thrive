from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.session import get_db
from src.repositories.user import UserRepository
from src.services.auth import AuthService
from src.models.pydantic.user import UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = AuthService(user_repo)

    return await service.register_new_user(user_data)

@router.get("/get_user", response_model=UserRead)
async def get_user(user_name: str ,db: AsyncSession = Depends(get_db)):
    """Get user by name."""
    user_repo = UserRepository(db)
    service = AuthService(user_repo)
    return await service.get_user_data(user_name)

@router.delete("/delete_user")
async def delete_user(user_name: str, db: AsyncSession = Depends(get_db)):
    """Deletes user by name."""
    user_repo = UserRepository(db)
    service = AuthService(user_repo)
    return await service.delete_user_by_name(user_name)

@router.put("/update_user_data")
async def update_user(user_name: str, new_name: str, db: AsyncSession = Depends(get_db)):
    """Updates user's name."""
    user_repo = UserRepository(db)
    service = AuthService(user_repo)
    return await service.update_username(user_name, new_name)