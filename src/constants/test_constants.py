from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR1 = "author1"
    AUTHOR2 = "author2"
    TEST_USER = "testuser"


class RoleT(int, Enum):
    ADMIN = 1
    AUTHOR = 2
    USER = 3
