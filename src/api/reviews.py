from fastapi import APIRouter

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ReviewAlreadyExistsException, ReviewAlreadyExistsHTTPException, BookNotFoundException, \
    BookNotFoundHTTPException
from src.schemas.reviews import ReviewAddRequestDTO
from src.services.reviews import ReviewsService

router = APIRouter(prefix="/books", tags=["Отзывы"])

@router.post("/{book_id}")
async def add_review(
        user: UserIdDep,
        db:DBDep,
        data: ReviewAddRequestDTO,
        book_id: int,
):
    try:
        review = await ReviewsService(db).add_review(
            user,
            book_id,
            data
        )
    except ReviewAlreadyExistsException:
        raise ReviewAlreadyExistsHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {
        "status": "success",
        "data": review
    }
