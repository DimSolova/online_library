from src.models import FavoriteOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import FavoriteDataMapper


class FavoriteRepository(BaseRepository):
    model = FavoriteOrm
    mapper = FavoriteDataMapper