from sqlalchemy import select

from src.models import BookOrm
from src.repositories.base import BaseRepository
from src.schemas.books import BookDTO


class BookRepository(BaseRepository):
    model = BookOrm
    schema = BookDTO

    async def get_filtered(self, limit, offset):
        query = (
            select(self.model)
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(query)
        model = res.scalars().all()
        return [self.schema.model_validate(book) for book in model]