from src.exceptions import (
    BookNotFoundException,
    ForeignKeyException,
    ObjectAlreadyExistsException,
    ReviewAlreadyExistsException,
)
from src.schemas.notifications import NotificationAddDTO
from src.schemas.reviews import ReviewAddDTO, ReviewAddRequestDTO
from src.services.base import BaseService
from src.tasks.tasks import send_notification_to_user


class ReviewsService(BaseService):
    async def add_review(self, user, book_id, data: ReviewAddRequestDTO):
        """При написании этого метода, когда мы отправляем celery task, нам рекомендуют
         не вызывать этот метод напрямую из этого сервиса, обратиться
        к сервису Notification и там написать эту логику"""
        add_review = ReviewAddDTO(**data.model_dump(), user_id=user.id, book_id=book_id)
        try:
            res = await self.db.review.add(add_review)

            #### Формирую pydantic схему для добавления уведомлений
            book = await self.db.books.get_one(id=book_id)
            user_id = book.added_by_id
            text = f"вашу книгу оценили в {data.rating}"

            send_notification_to_user.delay(  # type: ignore[attr-defined]
                user_id=user_id, title=text, message=data.text, related_book_id=book_id, related_review_id=res.id
            )
            #
            await self.db.commit()

        except ObjectAlreadyExistsException:
            raise ReviewAlreadyExistsException
        except ForeignKeyException:
            raise BookNotFoundException

        return res

    async def delete_review(self, review_id):
        await self.db.review.delete(id=review_id)
        await self.db.commit()
