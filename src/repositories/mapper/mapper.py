from src.models import BookOrm, ReviewOrm, RoleOrm, UserOrm, FavoriteOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.books import BookDTO, BookWithRelsDTO
from src.schemas.favorites import FavoriteDTO
from src.schemas.reviews import ReviewDTO
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


class BookWithRelsMapper(DataMapper):
    db_model = BookOrm
    schema = BookWithRelsDTO


class RoleDataMapper(DataMapper):
    db_model = RoleOrm
    schema = RoleDTO


class ReviewDataMapper(DataMapper):
    db_model = ReviewOrm
    schema = ReviewDTO

class FavoriteDataMapper(DataMapper):
    db_model = FavoriteOrm
    schema = FavoriteDTO