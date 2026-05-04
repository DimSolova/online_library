from src.api.dependencies import AuthorOrAdminDep
from src.constants.roles import UserRole
from src.exceptions import (
    BookNotFoundException,
    ISBNAlreadyExistsException,
    NotBookOwnerException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from src.schemas.books import BookAddRequestDTO, BookDTO, BookDTOAdd, BookPATCHDTO
from src.schemas.users import UserTokenDTO
from src.services.base import BaseService


class BooksService(BaseService):
    async def check_author(self, user: UserTokenDTO, book_id: int):
        """Если авторизован как админ, то пропускаем этот блок
        Если автор, то делаем запрос в БД на проверку автора"""
        if user.role == UserRole.ADMIN:
            return
        book: BookDTO | None = await self.db.books.get_one_or_none(id=book_id)
        if book is None:
            raise BookNotFoundException
        if book.added_by_id != user.id:
            raise NotBookOwnerException

    async def get_book(self, book_id: int) -> BookDTO:
        try:
            book = await self.db.books.get_one(id=book_id)
        except ObjectNotFoundException:
            raise BookNotFoundException
        return book

    async def get_books(self, pagination, title: str | None, author: str | None):

        page = pagination.page
        per_page = pagination.per_page or 5
        books = await self.db.books.get_filtered_pag(
            limit=per_page, offset=per_page * (page - 1), title=title, author=author
        )
        return books

    async def add_book(self, user: AuthorOrAdminDep, data: BookAddRequestDTO):
        """Добавляет новую книгу в библиотеку.

        Args:
            user: Текущий пользователь (из зависимости UserRoleDep)
            data: Данные книги из запроса

        Returns:
            BookDTO: Созданная книга со всеми полями

        Raises:
            ISBNAlreadyExistsException: Если книга с таким ISBN уже существует
        """
        user_data = BookDTOAdd(
            title=data.title,
            description=data.description,
            isbn=data.isbn,
            author=data.author,
            added_by_id=user.id,
        )
        try:
            res = await self.db.books.add(user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise ISBNAlreadyExistsException
        return res

    async def edit_book(self, data: BookAddRequestDTO, user: UserTokenDTO, book_id: int):
        await self.check_author(user, book_id)
        """В API service и repository повторяется одна и таже проверка ошибки
        Добавил проверку ошибки точно такую же как и в add очень много повтора получается,
         это 100% надо куда-то вынести"""
        try:
            book = await self.db.books.edit(data, id=book_id)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise ISBNAlreadyExistsException
        return book

    async def partially_edit_book(self, data: BookPATCHDTO, user: UserTokenDTO, book_id: int):
        """exclude_unset метод в pydantic, позволяет не записывать NULL в таблицу"""
        await self.check_author(user, book_id)
        try:
            book = await self.db.books.edit(data, exclude_unset=True, id=book_id)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise ISBNAlreadyExistsException
        return book

    async def delete_book(self, user, book_id: int):
        await self.check_author(user, book_id)
        await self.db.books.delete(id=book_id)
        await self.db.commit()
