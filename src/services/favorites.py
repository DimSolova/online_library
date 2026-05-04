from src.schemas.favorites import FavoriteAddDTO
from src.services.base import BaseService


class FavoritesServices(BaseService):
    async def get_favorites(self, user):
        favorites_dto = await self.db.favorites.get_filtered(user_id=user.id)
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

    async def delete_favorite(self, user, book_id):
        await self.db.favorites.delete(user_id=user.id, book_id=book_id)
        await self.db.commit()
