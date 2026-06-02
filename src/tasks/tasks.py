import asyncio
import os
from time import sleep

from PIL import Image

from src.database import async_session_maker, async_session_maker_null_pool
from src.init import redis_manager
from src.schemas.notifications import NotificationAddDTO
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        print(size)
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)
        new_file_name = f"{name}_{size}px{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f"Изображение сохраненно в следующих размерах: {sizes} в папке {output_folder}")


async def send_emails_to_users_with_favorites_helper(user_id):
    print("Я Запускаюсь")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        books = await db.books.get_favorite_books(user_id)
        print(books)


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_favorites_books(user_id):
    print(user_id)
    # что бы запустить асинхронный код внутри синхронного, самый известный метод
    asyncio.run(send_emails_to_users_with_favorites_helper(user_id))


### таска на добавление уведомлений
async def send_notification_to_users_with_helper(user_id, title, message, related_book_id, related_review_id):
    data = NotificationAddDTO(
        user_id=user_id,
        title=title,
        message=message,
        related_book_id=related_book_id,
        related_review_id=related_review_id,
    )
    print("Собрал pydantic схему, запускаем сессию без пула")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.notifications.add(data)
        print("Данные добавлены")


### Таска на отправку уведомлений автору книги
@celery_instance.task
def send_notification_to_user(user_id: int, title: str, message: str, related_book_id: int, related_review_id: int):
    print("отправляем уведомление")
    asyncio.run(send_notification_to_users_with_helper(user_id, title, message, related_book_id, related_review_id))


### Таска для удаления всего кеша
@celery_instance.task(name="clear_all_cache")
def clear_all_cache():

    async def clear_cache():
        await redis_manager.connect()
        keys = await redis_manager.get_all_keys()
        await redis_manager.delete_all_keys(keys)

    asyncio.run(clear_cache())
