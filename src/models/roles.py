from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class RoleOrm(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # __repr__ — специальный метод, который вызывается, когда ты печатаешь объект в консоли
    # или в отладчике. Очень удобно видеть читаемое представление вместо "<Role object at 0x...>"
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"
