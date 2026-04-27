from src.constants.roles import UserRole
from src.exceptions import ObjectAlreadyExistsException, ISBNAlreadyExistsException, NotBookOwnerException, \
    BookNotFoundException
from src.schemas.books import BookDTOAdd, BookDTO, BookAddRequestDTO, BookPATCHDTO
from src.schemas.users import UserTokenDTO
from src.services.base import BaseService


class BooksService(BaseService):

    async def check_author(self, user, book_id):
        """Если авторизован как админ, то пропускаем этот блок
            Если автор, то делаем запрос в БД на проверку автора"""
        if user.role == UserRole.ADMIN:
            return
        book: BookDTO = await self.db.books.get_one_or_none(id=book_id)
        if book is None:
            raise BookNotFoundException
        if book.added_by_id != user.id:
            raise NotBookOwnerException

    async def get_books(self):

        books = await self.db.books.get_all()
        return books

    async def add_book(self,user, data):
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
            added_by_id=user.id
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
            book = await self.db.books.edit(data, exclude_unset=True,  id=book_id)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise ISBNAlreadyExistsException
        return book

    async def delete_book(self, user, book_id: int):
        await self.check_author(user, book_id)
        await self.db.books.delete(id=book_id)
        await self.db.commit()
