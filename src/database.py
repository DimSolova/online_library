from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import setting

engine = create_async_engine(setting.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
