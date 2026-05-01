from fastapi import APIRouter, Query

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.reviews import ReviewAddRequestDTO
from src.services.reviews import ReviewsService

router = APIRouter(prefix="/books", tags=["Отзывы"])

@router.post("/{book_id}")
async def add_review(
        user: UserIdDep,
        db:DBDep,
        data: ReviewAddRequestDTO,
        book_id = int,
):
    review = await ReviewsService(db).add_review(
        book_id,
        data
    )
    return {
        "status": "success",
        "data": review
    }
