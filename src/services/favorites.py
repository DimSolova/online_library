from src.schemas.favorites import FavoriteAddDTO
from src.services.base import BaseService


class FavoritesServices(BaseService):

    async def get_favorites(self, user):
        favorites_dto = await self.db.favorites.get_one_or_none(user_id=user.id)
        return favorites_dto

    async def add_favorites(
            self,
            user,
            book_id,
    ):
        favorite_dto = FavoriteAddDTO(user_id=user.id, book_id=book_id)
        res = await self.db.favorites.add(favorite_dto)
        await self.db.commit()
        return res
