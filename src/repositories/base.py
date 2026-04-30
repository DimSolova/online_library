import logging
from typing import NoReturn

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    ForeignKeyException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    handle_db_integrity_error,
    raise_integrity_error,
)
from src.models.base import Base
from src.repositories.mapper.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        try:
            res = await self.session.execute(query)
            model = res.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        data = res.scalars().all()
        return [self.mapper.map_to_domain_entity(book) for book in data]

    async def add(self, data):
        data_dict = data.model_dump()
        add_stmt = insert(self.model).values(**data_dict).returning(self.model)
        # print(add_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError as ex:
            raise_integrity_error(ex, "add")
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        """В API service и repository повторяется одна и таже проверка ошибки
        Добавил проверку ошибки точно такую же как и в add очень много повтора получается,
         это 100% надо куда-то вынести"""
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        try:
            res = await self.session.execute(update_stmt)
        except IntegrityError as ex:
            raise_integrity_error(ex, "edit")
        try:
            model = res.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter):
        delete_stmt = delete(self.model).filter_by(**filter)
        await self.session.execute(delete_stmt)
