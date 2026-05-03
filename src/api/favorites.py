from fastapi import APIRouter

router = APIRouter(prefix="/favorites", tags=["Избранное"])


@router.post("/{book_id}")
async def add_favorites(book_id):
    return {
        "status": "success",
        "data": book_id
    }

