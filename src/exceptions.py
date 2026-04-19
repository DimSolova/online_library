

from fastapi import HTTPException

class LibraryException(Exception):
    detail = "Error"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ObjectAlreadyExistsException(LibraryException):
    detail = "Объект уже существует"

class UserAlreadyExistsException(LibraryException):
    detail = "email уже существует"

class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = "Object not found"
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Пользователь с таким email существует"