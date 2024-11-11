from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from contextlib import asynccontextmanager
<<<<<<< HEAD
=======
>>>>>>> main

from .config import DB_URL


engine = create_async_engine(DB_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
