from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models import BookOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import BookDataMapper, BookWithRelsMapper


class BookRepository(BaseRepository):
    model = BookOrm
    mapper = BookDataMapper

    async def get_filtered(
        self,
        limit,
        offset,
        title,
        author,
    ):
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
