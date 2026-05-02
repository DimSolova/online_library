from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "14004630f3d4"
down_revision: Union[str, Sequence[str], None] = "33b9556cabf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "reviews",
        "text",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=500),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "reviews",
        "text",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
    )
