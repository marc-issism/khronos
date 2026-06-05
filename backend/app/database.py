from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import aiosqlite as aiosqlite

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./khronos.db" #TODO: Swap to postgres
# +aiosqlite is the async engine

# DATABASE = 'postgresql'
# USER = 'postgres'
# PASSWORD = 'your password'
# HOST = 'localhost'
# PORT = '5432'
# DB_NAME = 'postgres'
# engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME }')


engine = create_async_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={"check_same_thread": False} #TODO: for sqlite only
)

AsyncSessionLocal = async_sessionmaker(
  engine, 
  class_ = AsyncSession,
  expire_on_commit = False,
)
# session = transaction with database, autocommit and autoflush = False allow US to control when changes happen

class Base(DeclarativeBase):
  pass


async def get_db():
  async with AsyncSessionLocal() as session: 
    yield session # gives this route a database session

DB = Annotated[AsyncSession, Depends(get_db)]