from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "1b5690406a26"
down_revision: Union[str, Sequence[str], None] = "839249b9ca1c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_user_book_favorite", "favorites", ["user_id", "book_id"])


def downgrade() -> None:
    op.drop_constraint("uq_user_book_favorite", "favorites", type_="unique")
