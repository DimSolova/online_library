

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

class InvalidTokenException(LibraryException):
    detail = "Вы не предоставили токен"

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

class TokenNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "токен не найден"