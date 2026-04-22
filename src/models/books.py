from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base   # твой базовый класс


class BookOrm(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(150), nullable=False)

    # ISBN — уникальный международный идентификатор книги (13 символов)
    # Можно оставить NULL, если ISBN неизвестен
    isbn: Mapped[str | None] = mapped_column(String(13), unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Если хочешь связать книгу с пользователем (например, кто добавил книгу в библиотеку)
    # Сейчас ты назвал поле author_id — это может ввести в заблуждение, потому что author — это уже строка с именем автора книги.
    # Лучше назвать added_by_id или owner_id
    added_by_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),    ##формат записи
        server_default="now()",     # PostgreSQL сам поставит текущее время при INSERT
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),     ##формат записи
        server_default="now()",      ## значение по умолчанию при создании
        onupdate=datetime.utcnow,    # автоматически обновляется при любом UPDATE
        nullable=False
    )

    # здесь нужен блок коментарий
    def __repr__(self) -> str:
        return f"<Book {self.id=} {self.title=} {self.author=} {self.isbn=} {self.added_by_id=}>"