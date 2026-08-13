"""Async PostgreSQL engine and session management."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from supplymind.shared.config.settings import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# -------------------
# Transaction scope
# -------------------

@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide one transactional session.

    The transaction commits on success and rolls back on exception.
    Repository implementations only `flush`; transaction ownership stays here.
    """

    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session


# -------------------
# Engine lifecycle
# -------------------

async def dispose_engine() -> None:
    """Dispose pooled database connections during application shutdown."""

    await engine.dispose()
