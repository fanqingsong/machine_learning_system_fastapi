

from .models import User
from ..db.session import get_session
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from demo.db.session import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# def get_user_db(session: Session = Depends(get_session)):
#     db = SQLAlchemyUserDatabase(session, User)
#     try:
#         yield db
#     finally:
#         # session.close()
#         pass

