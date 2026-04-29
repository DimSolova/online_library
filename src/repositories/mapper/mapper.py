from src.models import UserOrm, BookOrm, RoleOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.books import BookDTO
from src.schemas.roles import RoleDTO
from src.schemas.users import UserDTO, UserWithHashDTO


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = UserDTO


class UserHashDataMapper(DataMapper):
    db_model = UserOrm
    schema = UserWithHashDTO


class BookDataMapper(DataMapper):
    db_model = BookOrm
    schema = BookDTO


class RoleDataMapper(DataMapper):
    db_model = RoleOrm
    schema = RoleDTO
