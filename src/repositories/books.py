from sqlalchemy import select

from src.models import BookOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import BookDataMapper


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
        query = select(self.model)
        if title:
            query = query.filter(BookOrm.title.contains(title))
        if author:
            query = query.filter(BookOrm.author.contains(author))
        query = query.limit(limit).offset(offset)
        res = await self.session.execute(query)
        model = res.scalars().all()
        return [self.mapper.map_to_domain_entity(book) for book in model]
