from enum import IntEnum


class UserRole(IntEnum):
    """Роли пользователей из таблицы roles
    Эти числа берутся из БД когда в ней роли уже созданы"""
    ADMIN = 1
    AUTHOR = 2
    USER = 3

    @property
    def can_manage_books(self) -> bool:
        """Может ли роль управлять книгами (создавать, редактировать, удалять)"""
        return self in (UserRole.ADMIN, UserRole.AUTHOR)

    @property
    def is_superuser(self) -> bool:
        """Суперпользователь (полные права)"""
        return self == UserRole.ADMIN