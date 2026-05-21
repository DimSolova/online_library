from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.database import engine
from src.models import BookOrm, FavoriteOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import BookDataMapper, BookWithRelsMapper


class BookRepository(BaseRepository):
    model = BookOrm
    mapper = BookDataMapper

    async def get_filtered_pag(
        self,
        limit,
        offset,
        title,
        author,
    ):
        """Получить список книг с фильтрацией и пагинацией.

        Возвращает книги вместе с отзывами (joinedload).

        Args:
            limit: Максимальное количество книг на странице.
            offset: Смещение для пагинации (номер страницы * limit).
            title: Фильтр по названию книги (частичное совпадение).
            author: Фильтр по имени автора (частичное совпадение).

        Returns:
            Список доменных сущностей книг с загруженными отзывами.
        Returns:
            Список доменных моделей Book с предзагруженным отношением `reviews`.
        Note:
            Используется `joinedload`, чтобы все отзывы были загружены
            в одном SQL-запросе.
        """
        query = (
            select(self.model).options(joinedload(self.model.reviews))  # type: ignore[attr-defined]
        )
        if title:
            query = query.filter(BookOrm.title.contains(title))
        if author:
            query = query.filter(BookOrm.author.contains(author))
        query = query.limit(limit).offset(offset)
        res = await self.session.execute(query)
        model = res.unique().scalars().all()
        return [BookWithRelsMapper.map_to_domain_entity(book) for book in model]

    async def get_favorite_books(self, user_id):
        books_user_id = (
            select(FavoriteOrm.book_id)
            .select_from(FavoriteOrm)
            .filter(FavoriteOrm.user_id == user_id)
            .cte("books_user_id")
        )
        favorite_book = (
            select(BookOrm)
            .select_from(BookOrm)
            .join(books_user_id, BookOrm.id == books_user_id.c.book_id)
            .cte("favorite_book")
        )
        query = select(favorite_book).select_from(favorite_book)
        res = await self.session.execute(query)
        return res
