


class DataMapper:
    db_model = None
    schema = None

    """Принимаем данные из Sqlalchemy и возвращаем  pydantic схему"""
    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    """Принимает pydantic схемы и возвращаем модель алхимии"""
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())