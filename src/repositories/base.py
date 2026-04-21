import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.exceptions import ObjectAlreadyExistsException
from src.models.base import Base


class BaseRepository:
    model: Base
    schema: BaseModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        query = (
            select(self.model)
        )
        res = await self.session.execute(query)
        data = res.scalars().all()
        return [self.schema.model_validate(book) for book in data]

    async def add(self, data):
        data_dict = data.model_dump()
        add_stmt = (
            insert(self.model)
            .values(**data_dict)
            .returning(self.model)
        )
        print(add_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError as ex:
            logging.error(
                f"Не удалось добавить данные в БД, {data} тип ошибки {type(ex.orig.__cause__)=}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.error(
                    f"Неизвестная ошибка, не удалось добавить данные в БД {data}тип ошибки  {type(ex.__cause__)=}")
                raise ex
        model = result.scalar_one()
        data = self.schema.model_validate(model)
        return data
