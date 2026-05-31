from sqlalchemy.exc import SQLAlchemyError

from src.repositories.books import BookRepository
from src.repositories.favorites import FavoriteRepository
from src.repositories.notifications import NotificationRepository
from src.repositories.reviews import ReviewRepository
from src.repositories.roles import RoleRepository
from src.repositories.users import UserRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.books = BookRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.review = ReviewRepository(self.session)
        self.favorites = FavoriteRepository(self.session)
        self.notifications = NotificationRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                # Если не было исключения — коммитим
                await self.session.commit()
            else:
                # Если было исключение — откатываем
                await self.session.rollback()
        ### возможно стоит обрабатывать ошибку по другому
        except SQLAlchemyError:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()

    async def commit(self):
        await self.session.commit()
