from fastapi import APIRouter, Query

from src.api.dependencies import AuthorOrAdminDep, DBDep, PaginationDep
from src.exceptions import (
    BookNotFoundException,
    BookNotFoundHTTPException,
    ISBNAlreadyExistsException,
    ISBNBookAlreadyExistsHTTPException,
    NotBookOwnerException,
    NotBookOwnerHTTPException,
)
from src.schemas.books import BookAddRequestDTO, BookPATCHDTO
from src.services.books import BooksService

router = APIRouter(prefix="/books", tags=["Книги"])

"""TODO 
В Ручках PUT PATCH DELETE повторяется обработка исключений,Скорее всего стоит это как-то вынести в отдельное место
Grok предложил сделать отдельную Depends на проверку этих ошибок
"""


@router.get("/{book_id}")
async def get_book(db: DBDep, book_id: int):
    try:
        book = await BooksService(db).get_book(book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {"status": "success", "data": book}


@router.get("")
async def get_books(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название книги"),
    author: str | None = Query(None, description="Автор книги"),
):
    books = await BooksService(db).get_books(pagination, title, author)
    return {"status": "success", "data": books}


@router.post("")
async def add_book(data: BookAddRequestDTO, user: AuthorOrAdminDep, db: DBDep):
    """Создается книга, Реализованна проверка на роль через Depends
    Является ли пользователь автором или админом
    Есть проверка на существующий ISBN
    """
    try:
        data = await BooksService(db).add_book(user, data)
    except ISBNAlreadyExistsException:
        raise ISBNBookAlreadyExistsHTTPException
    return {"status": "ok", "data": data}


@router.put("/{book_id}")
async def edit_book(
    book_id: int,
    data: BookAddRequestDTO,
    user: AuthorOrAdminDep,
    db: DBDep,
):
    """Полное редактирование Книги
    Проверет авторизацию пользователя
    Есть вроверка на контретного автора через запрос к БД"""
    try:
        editing_book = await BooksService(db).edit_book(data, user, book_id)
    except NotBookOwnerException:
        raise NotBookOwnerHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except ISBNAlreadyExistsException:
        raise ISBNBookAlreadyExistsHTTPException

    return {"status": "success", "data": editing_book}


@router.patch("/{book_id}")
async def partially_edit_book(
    book_id: int, data: BookPATCHDTO, user: AuthorOrAdminDep, db: DBDep
):
    """Частичное редактирование книги
    проверяем JWT token
    Есть проверка на конкретного автора через запрос к БД"""
    try:
        update_book = await BooksService(db).partially_edit_book(data, user, book_id)
    except NotBookOwnerException:
        raise NotBookOwnerHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except ISBNAlreadyExistsException:
        raise ISBNBookAlreadyExistsHTTPException

    return {"status": "success", "data": update_book}


@router.delete("/{book_id}")
async def delete_book(book_id: int, user: AuthorOrAdminDep, db: DBDep):
    try:
        await BooksService(db).delete_book(user, book_id)
    except NotBookOwnerException:
        raise NotBookOwnerHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {
        "status": "success",
        "data": f"книга с id:{book_id} удалена",
    }
