from fastapi import APIRouter

from src.api.dependencies import AdminDep, DBDep, UserIdDep
from src.exceptions import (
    BookNotFoundException,
    BookNotFoundHTTPException,
    ReviewAlreadyExistsException,
    ReviewAlreadyExistsHTTPException,
)
from src.schemas.reviews import ReviewAddRequestDTO
from src.services.reviews import ReviewsService

router = APIRouter(prefix="/books", tags=["Отзывы"])


@router.post("/{book_id}")
async def add_review(
    user: UserIdDep,
    db: DBDep,
    data: ReviewAddRequestDTO,
    book_id: int,
):
    try:
        review = await ReviewsService(db).add_review(user, book_id, data)
    except ReviewAlreadyExistsException:
        raise ReviewAlreadyExistsHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {"status": "success", "data": review}


@router.delete("/{review_id}/review")
async def delete_review(
    user: AdminDep,
    db: DBDep,
    review_id: int,
):
    await ReviewsService(db).delete_review(review_id)
    return {"status": "success", "data": f"отзыв по id:{review_id} удален"}
