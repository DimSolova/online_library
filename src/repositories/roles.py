from src.models import RoleOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import RoleDataMapper


class RoleRepository(BaseRepository):
    model = RoleOrm
    mapper = RoleDataMapper
