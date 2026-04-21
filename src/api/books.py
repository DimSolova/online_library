from fastapi import APIRouter

from src.api.dependencies import UserRoleDep, DBDep
from src.exceptions import ISBNAlreadyExistsException, ISBNBookAlreadyExistsHTTPException
from src.schemas.books import AddBookRequestDTO, BookAdd
from src.services.books import BooksService

router = APIRouter(prefix="/books", tags=["Книги"])

@router.get("")
async def get_books(db:DBDep):
    books = await BooksService(db).get_books()
    return {
        "status": "success",
        "data": books
            }

@router.post("")
async def add_book(
        data: AddBookRequestDTO,
        user: UserRoleDep,
        db: DBDep
):
    """Создаёт новую книгу в библиотеке.
        Требует авторизации пользователя.
        Args:
            data: Данные новой книги
            user: Текущий авторизованный пользователь
            db: Сессия базы данных
        Returns:
            dict: {"status": "ok", "data": BookDTO}
        Raises: ISBNBookAlreadyExistsHTTPException: Если ISBN уже существует
        """
    try:
        data = await BooksService(db).add_book(user, data)
    except ISBNAlreadyExistsException:
        raise ISBNBookAlreadyExistsHTTPException
    return {
        "status": "ok",
        "data": data
    }

@router.put("/{book_id}")
async def edit_book(
        book_id: int,
        data: BookAdd,
        db: DBDep,
):
    await BooksService(db).edit_book(data, book_id)
    return {
        "status": "success",
        "data": data
    }

@router.delete("/{book_id}")
async def delete_book(
        book_id: int,
        db: DBDep
):
    await BooksService(db).delete_book(book_id)
    return {
        "status": "success",
            "data": book_id,
    }

