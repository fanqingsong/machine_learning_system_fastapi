from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from demo.core.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_URI_ASYNC
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator



engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={'check_same_thread': False})
session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)

engine_async = create_async_engine(SQLALCHEMY_DATABASE_URI_ASYNC)
async_session_maker = sessionmaker(engine_async, class_=AsyncSession, expire_on_commit=False)


def get_session() -> Session:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

