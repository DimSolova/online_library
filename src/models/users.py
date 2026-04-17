from datetime import datetime

from sqlalchemy import BigInteger, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


from src.models import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # is_active — флаг, активен ли пользователь (можно ли ему логиниться)
    # default=True → значение по умолчанию в Python (когда создаём объект через SQLAlchemy)
    # server_default="true" → значение по умолчанию прямо в базе данных (на случай, если запись создаётся не через SQLAlchemy)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,     # значение по умолчанию в Python-коде
        server_default="true",  # значение по умолчанию на уровне PostgreSQL
        nullable = False
    )

    # created_at — дата и время создания пользователя
    # DateTime(timezone=True)→ хранит время с учётом часового пояса (рекомендуется)
    # default=datetime.utcnow→ если мы создаём объект в Python, автоматически подставит текущее время
    # server_default="now()"→ если запись создаётся напрямую в базе (например через INSERT), база сама поставит текущее время
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),   #формат записи
        default=datetime.utcnow,  # Python-side default
        server_default="now()",    # Database-side default
        nullable=False
    )

    # role_id — внешний ключ, который ссылается на таблицу roles
    # ondelete="SET NULL"→ что делать, если роль, на которую ссылается пользователь, будет удалена?
    #В этом случае у пользователя просто очистится role_id (станет NULL),
    #вместо того чтобы удалить самого пользователя или вызвать ошибку.
    role_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="SET NULL"),   # что такое ondelete
        nullable=True
    )

    # __repr__ — удобное текстовое представление объекта при печати (для отладки)
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"