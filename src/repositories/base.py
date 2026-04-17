from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.models import Base


class BaseRepository:
    model: Base
    schema: BaseModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data):
        data_dict = data.model_dump()
        add_stmt = (
            insert(self.model)
            .values(**data_dict)
        )
        # print(add_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_stmt)
