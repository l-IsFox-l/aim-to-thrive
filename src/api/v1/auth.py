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

