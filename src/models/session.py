from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.utils.settings import settings

# Create engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()