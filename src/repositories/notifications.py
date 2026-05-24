from src.models import NotificationOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import NotificationDataMapper


class NotificationRepository(BaseRepository):
    model = NotificationOrm
    mapper = NotificationDataMapper
