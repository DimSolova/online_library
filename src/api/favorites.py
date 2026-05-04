from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.services.favorites import FavoritesServices

router = APIRouter(prefix="/favorites", tags=["Избранное"])


@router.get("")
async def get_favorites(
    user: UserIdDep,
    db: DBDep,
):
    my_favorites = await FavoritesServices(db).get_favorites(user)
    return {"status": "success", "data": my_favorites}


@router.post("/{book_id}")
async def add_favorites(user: UserIdDep, db: DBDep, book_id: int):
    favorites = await FavoritesServices(db).add_favorites(user, book_id)
    return {"status": "success", "data": favorites}


@router.delete("/{book_id}")
async def delete_favorite(user: UserIdDep, db: DBDep, book_id: int):
    await FavoritesServices(db).delete_favorite(user, book_id)
    return {"status": "success", "data": f"книга с id: {book_id} удалена из избранного"}
