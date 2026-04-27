from enum import Enum

class TestUser(str, Enum):
    ADMIN = "admin"
    AUTHOR1 = "author1"
    AUTHOR2 = "author2"
    TEST_USER = "testuser"

class TestRole(int, Enum):
    ADMIN = 1
    AUTHOR = 2
    USER = 3