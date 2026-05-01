import pytest

from src.api.dependencies import PaginationParams, get_current_user
from src.schemas.books import BookAddRequestDTO, BookDTO
from src.services.books import BooksService
from test.helpers.auth import login_as_author


async def test_get_book(db):
    book = await db.books.get_all()
    book_id = book[0].id
    assert book_id

    book_dto = await BooksService(db).get_book(book_id)
    assert book_dto

    assert book_dto.id == book_id
    assert book_dto.title
    assert len(book_dto.isbn) <= 13
    assert book_dto.author
    assert isinstance(book_dto, BookDTO)


@pytest.mark.parametrize(
    "page, per_page, title, author",
    [
        (1, 2, None, None),
        (1, 3, None, None),
        (1, None, None, None),
    ],
)
async def test_get_books(page, per_page, title, author, db):
    pagination = PaginationParams(page=page, per_page=per_page)

    books = await BooksService(db).get_books(pagination, title=title, author=author)
    assert books
    count = per_page or 5
    assert len(books) == count


async def test_add_book(ac, db):
    resp_author = await login_as_author(ac, "author1")
    token = resp_author.cookies["access_token"]
    user = get_current_user(token)
    user_data = BookAddRequestDTO(
        title="Бесы",
        description="Книга о Бесах",
        isbn="1234567890987",
        author="Ф.М. Достоевский",
    )
    book_dto = await BooksService(db).add_book(user, user_data)
    assert book_dto.title
    assert len(book_dto.isbn) <= 13
    assert book_dto.author
    assert isinstance(book_dto, BookDTO)


async def test_edit_book(ac, db):
    book = await db.books.get_all()
    book_id = book[0].id
    assert book_id

    resp_author = await login_as_author(ac, "author1")
    token = resp_author.cookies["access_token"]
    user = get_current_user(token)

    user_data = BookAddRequestDTO(
        title="Бес",
        description="Книга о Бесах",
        isbn="1234567890986",
        author="Другой автор",
    )
    book_dto = await BooksService(db).edit_book(user_data, user, book_id)
    assert book_dto.title
    assert len(book_dto.isbn) <= 13
    assert book_dto.author
    assert isinstance(book_dto, BookDTO)
