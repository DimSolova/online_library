from typing import TypeVar, Generic

from pydantic import BaseModel

from src.models import Base

"""Мы создаем именованные переменные типов, сперциальный placeholder
помогает pyright узнать что будет находится тип BaseModel или Base
и будет наследоваться от них"""
SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper(Generic[DBModelType, SchemaType]):
    """Для помощи pyright, что бы он понимал от какого типа может наследоваться"""

    db_model: type[DBModelType]
    schema: type[SchemaType]

    """Принимаем данные из Sqlalchemy и возвращаем  pydantic схему"""

    @classmethod
    def map_to_domain_entity(cls, data) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    """Принимает pydantic схемы и возвращаем модель алхимии"""

    @classmethod
    def map_to_persistence_entity(cls, data: SchemaType) -> DBModelType:
        return cls.db_model(**data.model_dump())
