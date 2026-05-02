import logging
from typing import NoReturn

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def handle_db_integrity_error(ex: IntegrityError, operation: str = "operation") -> None:
    """Централизованная обработка IntegrityError из SQLAlchemy + asyncpg"""
    cause = ex.orig.__cause__ if ex.orig is not None else None

    if isinstance(cause, UniqueViolationError):
        logging.warning(f"[{operation}] Нарушение уникальности: {ex}")
        raise ObjectAlreadyExistsException from ex

    if isinstance(cause, ForeignKeyViolationError):
        logging.warning(f"[{operation}] Нарушение внешнего ключа: {ex}")
        raise ForeignKeyException from ex

    logging.error(f"[{operation}] Неизвестная IntegrityError: {ex}")
    raise ex


def raise_integrity_error(ex: IntegrityError, operation: str) -> NoReturn:
    """Помогает pyright понять, что дальше код не выполнится"""
    handle_db_integrity_error(ex, operation=operation)
    raise RuntimeError("Unreachable code")  # только для type checker


# ====================== БАЗОВЫЕ ИСКЛЮЧЕНИЯ ======================


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

class ReviewAlreadyExistsException(LibraryException):
    detail = "Вы уже оставили отзыв"


class InvalidCredentialsException(LibraryException):
    detail = "Неверный Логин или пароль"


class ForeignKeyException(LibraryException):
    detail = "Ошибка ввода"


class InvalidRoleException(LibraryException):
    detail = "Неверная роль"


class ObjectNotFoundException(LibraryException):
    detail = "Объект не найден"


class BookNotFoundException(LibraryException):
    detail = "Книга не найдена"


class UserNotFoundException(LibraryException):
    detail = "Пользователь не найдена"


class InvalidTokenException(LibraryException):
    detail = "Вы не предоставили токен"


class NotBookOwnerException(LibraryException):
    detail = "Вы не являетесь владельцем этой книги"


# ====================== HTTP ИСКЛЮЧЕНИЯ ======================
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

class ReviewAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Вы уже оставили отзыв"


class InvalidCredentialsHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверный Логин или Пароль"


class InvalidTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверный токен"


class BookNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Книга не найдена"


class UserNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Пользователь не найден"


class TokenNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Вы не авторизованы"


class RoleForbiddenHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Доступ запрещён"

    def __init__(self, required_roles: list[str] | None = None):
        if required_roles:
            self.detail = f"Доступ запрещён. Требуется роль: {required_roles}"
        super().__init__()  # важно вызвать родительский __init__


class NotBookOwnerHTTPException(LibraryHTTPException):
    """403 - Пользователь пытается редактировать/удалять не свою книгу"""

    status_code = 403
    detail = "Вы не являетесь владельцем этой книги"


class BlockActiveHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Вы заблокированы"


class InvalidRoleHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверная роль"
