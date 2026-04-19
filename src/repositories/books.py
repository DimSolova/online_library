from src.models import BookOrm
from src.repositories.base import BaseRepository
from src.schemas.books import BookDTO


class BookRepository(BaseRepository):
    model = BookOrm
    schema = BookDTO