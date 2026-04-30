from src.utils.db_manager import DBManager


class BaseService:
    """
    Базовый класс для всех сервисов.
    db инжектится через Depends в FastAPI или передаётся вручную в тестах.
    """

    db: DBManager

    def __init__(self, db: DBManager | None = None):
        """db может быть None только в unit-тестах, где не используется БД"""
        self.db = db  # type: ignore  # pyright будет знать, что в runtime db всегда есть
