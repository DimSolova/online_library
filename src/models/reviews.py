from datetime import datetime

from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class ReviewOrm(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  ##формат записи
        server_default="now()",  # PostgresSQL сам поставит текущее время при INSERT
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  ##формат записи
        server_default="now()",  ## значение по умолчанию при создании
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_user_book_review"),
    )