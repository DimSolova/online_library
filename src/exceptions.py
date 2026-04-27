from fastapi import HTTPException

class LibraryException(Exception):
    detail = "Error"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ObjectAlreadyExistsException(LibraryException):
    detail = "Объект уже существует"

class UserAlreadyExistsException(LibraryException):
    detail = "email уже существует"

class ISBNAlreadyExistsException(LibraryException):
    detail = "Книга с таким ISBN уже существует"

class InvalidCredentialsException(LibraryException):
    detail = "Неверный Логин или пароль"

class ObjectNotFoundException(LibraryException):
    detail = "Объект не найден"

class BookNotFoundException(LibraryException):
    detail = "Книга не найдена"

class InvalidTokenException(LibraryException):
    detail = "Вы не предоставили токен"

class NotBookOwnerException(LibraryException):
    detail = "Вы не являетесь владельцем этой книги"

"""Исключения для FastAPI"""
class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = "Object not found"
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Пользователь с таким email существует"

class ISBNBookAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Книга с таким ISBN уже существует"

class InvalidCredentialsHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверный Логин или Пароль"

class InvalidTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверный токен"

class BookNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Книга не найдена"

class TokenNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "токен не найден"

class RoleForbiddenHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Доступ запрещён"

    def __init__(self, required_roles: list[str] | None = None):
        if required_roles:
            self.detail = f"Доступ запрещён. Требуется роль: {required_roles}"
        super().__init__()   # важно вызвать родительский __init__

class NotBookOwnerHTTPException(LibraryHTTPException):
    """403 - Пользователь пытается редактировать/удалять не свою книгу"""
    status_code = 403
    detail = "Вы не являетесь владельцем этой книги"