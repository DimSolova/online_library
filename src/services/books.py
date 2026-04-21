from src.exceptions import ObjectAlreadyExistsException, ISBNAlreadyExistsException
from src.schemas.books import BookAdd
from src.services.base import BaseService


class BooksService(BaseService):

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

    async def get_books(self):

        books = await self.db.books.get_all()
        return books