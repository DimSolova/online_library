from src.models import ReviewOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import ReviewDataMapper


class ReviewRepository(BaseRepository):
    model = ReviewOrm
    mapper = ReviewDataMapper
