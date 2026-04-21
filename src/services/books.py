from src.exceptions import ObjectAlreadyExistsException, ISBNAlreadyExistsException
from src.schemas.books import BookAdd
from src.services.base import BaseService


class BooksService(BaseService):

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
        user_data = BookAdd(
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

    """функция для полного изменения данных"""
    async def edit_book(self,data, book_id):
        await self.db.books.edit(data, id=book_id)
        await self.db.commit()

    async def partially_edit_book(self, data, book_id):
        book = await self.db.books.edit(data, exclude_unset=True,  id=book_id)
        await self.db.commit()
        return book

    async def delete_book(self, book_id: int):
        await self.db.books.delete(id=book_id)
        await self.db.commit()
