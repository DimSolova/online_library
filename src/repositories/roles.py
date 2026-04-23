from src.models import RoleOrm
from src.repositories.base import BaseRepository
from src.schemas.roles import RoleDTO


class RoleRepository(BaseRepository):
    model = RoleOrm
    schema = RoleDTO

