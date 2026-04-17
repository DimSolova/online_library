from src.models import UserOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserDTO


class UserRepository(BaseRepository):
    model = UserOrm
    schema = UserDTO