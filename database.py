from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator, Annotated
from dmodels import Base
from dotenv import load_dotenv
from project_util import getEnviromentVariable

load_dotenv()
def createDatabase(env_var_name:str):
    dbase_url:str = getEnviromentVariable(env_var_name)
    return create_async_engine(dbase_url , echo = True)



engine = createDatabase("DATABASE_URL")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
      await db.close()


DB = Annotated[AsyncSession, Depends(get_db)]