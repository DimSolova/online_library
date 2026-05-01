from fastapi import APIRouter


router = APIRouter(prefix="/books", tags=["Отзывы"])

@router.post("/{book_id}")
async def add_review():

    return {
        "status": "success",
        "data": "отзыв добавлен"
    }
