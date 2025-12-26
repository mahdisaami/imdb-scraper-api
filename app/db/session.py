from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "postgresql+asyncpg://mahdi@localhost:5432/imdb"


# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )
#
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# engine = create_async_engine(DATABASE_URL, echo=True)
#
# AsyncSessionLocal = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # dev only
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)