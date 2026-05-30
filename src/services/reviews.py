from src.exceptions import (
    BookNotFoundException,
    ForeignKeyException,
    ObjectAlreadyExistsException,
    ReviewAlreadyExistsException,
)
from src.schemas.notifications import NotificationAddDTO
from src.schemas.reviews import ReviewAddDTO, ReviewAddRequestDTO
from src.services.base import BaseService


class ReviewsService(BaseService):
    async def add_review(self, user, book_id, data: ReviewAddRequestDTO):
        add_review = ReviewAddDTO(**data.model_dump(), user_id=user.id, book_id=book_id)
        try:
            res = await self.db.review.add(add_review)

            #### Пишу откровенный говонокод на добавлени
            book = await self.db.books.get_one(id=book_id)
            #### Пишу откровенный говонокод на добавлени
            user_id = book.added_by_id
            text = f"вашу книгу оценили в {data.rating}"
            message = data.text
            rel_book_id = book_id


            notifications = NotificationAddDTO(
                user_id=user_id,
                title=text,
                message=message,
                related_book_id=rel_book_id,
                related_review_id=res.id
            )
            await self.db.notifications.add(notifications)

            await self.db.commit()

        except ObjectAlreadyExistsException:
            raise ReviewAlreadyExistsException
        except ForeignKeyException:
            raise BookNotFoundException

        return res

    async def delete_review(self, review_id):
        await self.db.review.delete(id=review_id)
        await self.db.commit()
