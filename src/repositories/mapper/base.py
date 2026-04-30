from typing import Generic, TypeVar

from pydantic import BaseModel

from src.models import Base

# ====================== TYPE VARIABLES ======================
"""
Эти TypeVar — "заполнители типов", которые позволяют нам создать универсальный маппер.

SchemaType — любой класс, который наследуется от BaseModel (Pydantic схема)
DBModelType — любой класс, который наследуется от Base (SQLAlchemy модель)
"""

SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper(Generic[DBModelType, SchemaType]):
    """
    Универсальный маппер между SQLAlchemy-моделями и Pydantic-схемами.

    Использование Generic позволяет pyright (и нам) понимать,
    с какими именно типами работает конкретный маппер в каждом репозитории.

    Пример использования:
        class UserMapper(DataMapper[UserOrm, UserDTO]):
            db_model = UserOrm
            schema = UserDTO

    Благодаря Generic pyright знает:
        - UserMapper.map_to_domain_entity() возвращает UserDTO
        - UserMapper.map_to_persistence_entity() принимает UserDTO
    """

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
